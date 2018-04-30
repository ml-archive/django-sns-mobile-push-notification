# Welcome to Django SNS Mobile Push Notifications.

Send push notifications to IOS and Android devices using Amazon SNS.

## Getting Started

### Installation

You can install sns_mobile_push_notification directly from pypi using pip:
```zsh
pip install django-sns-mobile-push-notification
```


Edit your settings.py file:

```python
INSTALLED_APPS = (
    ...
    "sns_mobile_push_notification",
)
```

## Required Settings

Login to AWS's SNS Dashboard and manually create 2 platform applications. One for IOS, and one for Android.
Add the following variables to your Django's settings file:

| Name | Description |
|------|-------------|
| ``AWS_ACCESS_KEY_ID`` | Access key of your AWS user. |
| ``AWS_SECRET_ACCESS_KEY`` | Secret key of your AWS user. |
| ``AWS_SNS_REGION_NAME`` | The region your SNS application is located in( e.g. 'eu-central-1'). |
| ``IOS_PLATFORM_APPLICATION_ARN`` | ARN for IOS platform application. |
| ``ANDROID_PLATFORM_APPLICATION_ARN`` | ARN for Android platform application. |


## Usage
```python
from sns_mobile_push_notification.models import Device
from sns_mobile_push_notification.tasks import register_device, refresh_device, send_sns_mobile_push_notification_to_device, deregister_device

# Given a valid token from Google's FCM(GCM), or Apple's APNs, create a device object.
device = Device()
device.token = "123456"
device.os = Device.IOS_OS
device.save()

# By registering a device, the token will be sent to SNS and SNS will return an ARN key which will be saved in the device object.
# ARN is required to send future push notification to SNS, regardless of the device type.
register_device(device)
device.refresh_from_db()
print(device.arn)

# You can refresh the device to make sure it is enabled and ready to use.
refresh_device(device)

# Now you can send the push notification to the the registered device.
if device.active and device.arn:
    send_sns_mobile_push_notification_to_device(
        device=device,
        notification_type="type",
        text="text",
        data={"a": "b"},
        title="title"
    )

# remove a device from SNS.
deregister_device(device)
```
