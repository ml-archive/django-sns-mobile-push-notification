def register_device(device):
    """
    Task that registers a device.
    :param device: device to be registered.
    :return: response from SNS
    """
    return device.register()


def deregister_device(device):
    """
    Task that deregisters a device.
    :param device: device to be deregistered.
    :return: response from SNS
    """
    return device.deregister()


def refresh_device(device):
    """
    Task that refreshes a device.
    :param device: device to be refreshed.
    :return: response from SNS
    """
    return device.refresh()


def send_sns_mobile_push_notification_to_device(device, notification_type, text, data, title):
    """
    Method that sends out a mobile push notification to a specific self.
    :param device: device to send the notification to.
    :param notification_type: type of notification to be sent
    :param text: text to be included in the push notification
    :param data: data to be included in the push notification
    :param title: title to be included in the push notification
    :return: response from SNS
    """
    return device.send(
        notification_type=notification_type,
        text=text,
        data=data,
        title=title
    )
