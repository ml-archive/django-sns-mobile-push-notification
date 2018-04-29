from django.db import models
from sns_mobile_push_notification.client import Client


class Device(models.Model):
    """
    Django model class representing a device.
    """

    # Constants
    IOS_OS = 0
    ANDROID_OS = 1
    OS_CHOICES = (
        (IOS_OS, 'IOS'),
        (ANDROID_OS, 'Android'),
    )

    # Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    os = models.IntegerField(choices=OS_CHOICES)
    token = models.CharField(max_length=255, unique=True)
    arn = models.CharField(max_length=255, unique=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    # Methods
    def __str__(self):
        """
        :return: string representation of this class.
        """
        return '%s device' % self.os_name

    # Metadata
    class Meta:
        ordering = ['-id']

    # Properties
    @property
    def is_android(self):
        return self.os == Device.ANDROID_OS

    @property
    def is_ios(self):
        return self.os == Device.IOS_OS

    @property
    def os_name(self):
        if self.is_android:
            return "ANDROID"
        elif self.is_ios:
            return "IOS"
        else:
            return "unknown"

    def register(self):
        """
        Method that registered a device on SNS for the first time,
        so that the device can receive mobile push notifications.
        it retrieves the endpoints ARN code and stores it.
        the ARN code will be used as the identifier for the device to send out mobile push notifications.
        :return: response from SNS
        """
        client = Client()
        if self.is_android:
            response = client.create_android_platform_endpoint(self.token)
        elif self.is_ios:
            response = client.create_ios_platform_endpoint(self.token)
        self.arn = response['EndpointArn']
        self.save(update_fields=['arn'])
        return response

    def refresh(self):
        """
        Method that checks/fixes the SNS endpoint corresponding a self.
        If the endpoint is deleted, disabled, or the it's token does not match the device token,
        it tries to recreate it.
        This task should be called upon a device update.
        :return: attributes retrieved from SNS
        """
        client = Client()
        try:
            attributes = client.retrieve_platform_endpoint_attributs(self.arn)
            endpoint_enabled = (attributes['Enabled'] == True) or (attributes['Enabled'].lower() == "true")
            tokens_matched = attributes['Token'] == self.token
            if not (endpoint_enabled and tokens_matched):
                client.delete_platform_endpoint(self.arn)
                self.register()
                attributes = client.retrieve_platform_endpoint_attributs(self.arn)
            return attributes
        except Exception as e:
            if 'Endpoint does not exist' in str(e):
                self.register()
                attributes = client.retrieve_platform_endpoint_attributs(self.arn)
                return attributes
            else:
                self.active = False
                self.save(update_fields=['active'])

    def deregister(self):
        """
        Method that deletes registered a device from SNS.
        :return: none
        """
        client = Client()
        client.delete_platform_endpoint(self.arn)
        self.active = False
        self.save(update_fields=['active'])

    def send(self, notification_type, text, data, title):
        """
        Method that sends out a mobile push notification to a specific self.
        :param notification_type: type of notification to be sent
        :param text: text to be included in the push notification
        :param data: data to be included in the push notification
        :param title: title to be included in the push notification
        :return: response from SNS
        """
        log = Log(
            device=self,
            notification_type=notification_type,
        )
        log.save()

        client = Client()

        if self.is_android:
            message, response = client.publish_to_android(
                arn=self.arn,
                text=text,
                title=title,
                notification_type=notification_type,
                data=data,
                id=log.id,
            )
        elif self.is_ios:
            message, response = client.publish_to_ios(
                arn=self.arn,
                text=text,
                title=title,
                notification_type=notification_type,
                data=data,
                id=log.id,
            )

        log.message = message
        log.response = response
        log.save()

        return response


class Log(models.Model):
    """
    Django model class representing a notification log.
    """

    # Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='notification_logs', null=True, blank=True)
    notification_type = models.CharField(max_length=255, null=True, blank=True)
    arn = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)

    # Methods
    def __str__(self):
        """
        :return: string representation of this class.
        """
        return '"%s" notification log for - "%s"' % (self.notification_type, self.device)