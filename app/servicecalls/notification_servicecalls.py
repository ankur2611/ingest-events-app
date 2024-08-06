from app.logger import logger


class NotificationServiceCall:

    @classmethod
    def notify_user(cls, user_id, event):
        # for now just logging the event, later lets notify user using API call.
        logger.info(f"NotificationServiceCall >> notify_user API Call for user_id: {user_id}, event: {event}")

    @classmethod
    def notify_operator(cls, event):
        # for now just logging the event, later lets notify operator using API call.
        operator_id = "some_operator_id"
        logger.info(f"NotificationServiceCall >> notify_operator API Call for operator_id: {operator_id}, event: {event}")
