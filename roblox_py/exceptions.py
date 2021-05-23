class NotFound(Exception):
    """ Not Found """
    pass


class PlayerNotFound(NotFound):
    """ Raised When Player  Not Found"""


class GamePassNotFound(NotFound):
    """ Raised When GamePass  Not Found"""


class GroupNotFound(NotFound):
    """ Raised When Group  Not Found"""


class BundleNotFound(NotFound):
    """ Raised When Bundle  Not Found"""


class BadgeNotFound(NotFound):
    """ Raised When Badge  Not Found"""


class GameNotFound(NotFound):
    """ Raised When Bundle  Not Found"""


class AssetNotFound(NotFound):
    """ Raised When Asset Is Not Found"""


class NotAuthenticated(Exception):
    """ Raised When User Not Authenticated"""


class HttpException(Exception):
    """ Http Error """
    pass


class InternalServiceError(HttpException):
    """500 HTTP error"""
    pass


class Unauthorized(HttpException):
    """401 HTTP error"""
    pass


class Forbidden(HttpException):
    """403 HTTP error"""
    pass


class RateLimited(HttpException):
    """429 HTTP error"""
    pass


class ServiceUnavailable(HttpException):
    """503 HTTP error"""
    pass


class UnknownError(HttpException):
    """ Unknown Error """
    pass


class BadRequest(NotFound):
    pass


class Captcha(Exception):
    """ Captcha Errors """
    pass


class InvalidAPIToken(Captcha):
    """Raised when the 2captcha api key is invalid"""
    pass


class InsufficientCredit(Captcha):
    """Raised when there is insufficient credit in 2captcha"""
    pass


class NoAvailableWorkers(Captcha):
    """Raised when there are no available workers"""
    pass


class IpBanned(Captcha):
    """
    Your IP address is banned due to many frequent attempts to access the server using wrong authorization keys.
    """


class IpNotAllowed(Captcha):
    """
    The request is sent from the IP that is not on the list of your allowed IPs.
    """


class MaxUserTurn(Captcha):
    """
    You made more than 60 requests to in.php within 3 seconds.
    Your account is banned for 10 seconds. Ban will be lifted automatically.
    """


class NNNNError(Captcha):
    """
    Where NNNN is numeric error code.
    You exceeded request limit and your account is temporary suspended.
    """


class BadProxy(Captcha):
    """
    You can get this error code when sending a captcha via proxy server which is marked as BAD by our API
    """


class UnsolvableCaptcha(Captcha):
    """
    We are unable to solve your captcha - three of our workers were unable solve it or we didn't get an answer within
    90 seconds (300 seconds for reCAPTCHA V2). We will not charge you for that request.
    """


class ReportNotRecorded(Captcha):
    """
    Error is returned to your report request if you already complained lots of correctly solved captchas (more than
    40%). Or if more than 15 minutes passed after you submitted the captcha.
    """


class IpAddressError(Captcha):
    """
    You can receive this error code when registering a pingback (callback) IP or domain. This happens if your request
    is coming from an IP address that doesn't match the IP address of your pingback IP or domain.
    """


class ProxyConnectionFailed(Captcha):
    """
    You can get this error code if we were unable to load a captcha through your proxy server. The proxy will be
    marked as BAD by our API and we will not accept requests with the proxy during 10 minutes. You will receive
    ERROR_BAD_PROXY code from in.php API endpoint in such case.
    """
