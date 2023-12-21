class TokenType:
    CUSTOMER_AUTH = 'CA'


class HeaderToken:
    ACCESS_TOKEN = 'HTTP_AUTHORIZATION'
    REFRESH_TOKEN = 'HTTP_RT'
    CUSTOMER_TOKEN = 'HTTP_CUSTOMERTOKEN'


class CookieToken:
    ACCESS_TOKEN = 'ct'
    REFRESH_TOKEN = 'rt'


class TokenExpiry:
    ONE_DAY_EXPIRE_SECONDS = 1 * 24 * 60 * 60 # 1 day
    ACCESS_EXPIRE_SECONDS = 60 * 2 # 2 minute
    REFRESH_EXPIRE_SECONDS = 60 * 60