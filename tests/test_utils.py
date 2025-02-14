import pytest
from urllib3 import HTTPResponse

from unofficial_livecounts_api.error import RequestApiError
from unofficial_livecounts_api.utils import send_request


def test_send_request_when_server_response_true(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.utils.http_client.request')
    mock_send_request.return_value = HTTPResponse(body=b'{"success": true}')
    data = send_request(url="http://test.test")
    mock_send_request.assert_called_once_with(
        method="GET",
        url="http://test.test",
        headers=mocker.ANY
    )
    assert data == {"success": True}


def test_send_request_when_server_response_false(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.utils.http_client.request')
    mock_send_request.return_value = HTTPResponse(body=b'{"success": false}')
    with pytest.raises(RequestApiError) as exec_info:
        send_request(url="http://test.test")
    mock_send_request.assert_called_once_with(
        method="GET",
        url="http://test.test",
        headers=mocker.ANY
    )
    assert str(exec_info.value) == "server response that it's not success, query: http://test.test"


def test_send_request_when_server_response_error(mocker):
    mock_send_request = mocker.patch('unofficial_livecounts_api.utils.http_client.request')
    mock_send_request.return_value = HTTPResponse(status=500)
    with pytest.raises(RequestApiError) as exec_info:
        send_request(url="http://test.test")
    mock_send_request.assert_called_once_with(
        method="GET",
        url="http://test.test",
        headers=mocker.ANY
    )
    assert str(exec_info.value) == "api server error, query: http://test.test"
