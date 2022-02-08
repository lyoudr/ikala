from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException

class CustomError(APIException):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, error_code=None, status_code=None, err_message = ''):
        if error_code:
            error_code = error_code
        if status_code:
            self.status_code = status_code


        self.detail = {
            'status_code': status_code,
            'error_code': error_code,
            'err_message': err_message,
        }


class CustomJsonResponse(JsonResponse):
    """CustomJsonResponse

    An HTTP response class that inherits JsonResponse
    :param res: A named_tuple imported from ci_admin.results.code_n_msg
                and passed to pay_load.
    :param data: A dictionary of kwargs passed to pay_load.
    :param pagination: The response of ci_admin.pagination.CustomPagination

    """
    def __init__(self, re_code='0000', re_message='', re_data={}, pagination={}, **kwargs):

        self.data = self.set_payload(re_code, re_message, re_data, pagination)
        super(CustomJsonResponse, self).__init__(
            data = self.data,
            **kwargs
        )

    def set_payload(self, re_code='0000', re_message='', re_data={}, pagination={}):
        payload = {
            're_code': re_code,
            're_message': re_message,
            're_data': re_data
        }
        
        if pagination:
            payload['pagination'] = pagination
        return payload