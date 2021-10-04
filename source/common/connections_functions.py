import random


def get_useragent():
    """
    This function returns a random user-agent to use in requests.
    :return: str user-agent
    """

    user_agent_list = [
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/77.0',
        "Mozilla/5.0 (Android 4.1.2; Mobile; rv:53.0.1) Gecko/53.0.1 Firefox/53.0.1",
        "Mozilla/5.0 (Linux; Android 9; moto g(6) plus Build/PPWS29.116-16-24; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 Instagram 156.0.0.26.109 Android (28/9; 540dpi; 1080x1998; motorola; moto g(6) plus; evert_nt; qcom; pt_BR; 240726484)",
        "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/84.0.4147.111 Mobile Safari/537.36 GSA/10.85.11.21.arm64",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; RMX2040) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36 OPR/59.1.2926.54067",
        "Mozilla/5.0 (Linux; Android 9; SM-G955F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 GSA/11.25.11.21.arm64",
        "Mozilla/5.0 (Linux; Android 7.0; PRO 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 5.1.1; LG-K130 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.1.0; SM-J260M Build/M1AJB; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; moto g(7) play Build/QPYS30.52-22-5; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 Instagram 157.0.0.37.120 Android (29/10; 320dpi; 720x1376; motorola; moto g(7) play; channel; qcom; pt_BR; 242168928)",
        "Mozilla/5.0 (Linux; Android 10; SM-M307F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/84.0.4147.89 Mobile Safari/537.36 GSA/11.24.10.21.arm64",
        "Mozilla/5.0 (Linux; Android 9; SM-S767VL Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 GSA/11.25.11.21.arm",
        "Mozilla/5.0 (Linux; Android 9; ONA19TB003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Safari/537.36",
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Linux; Android 5.1; LG-X190 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; LG-X190 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; LG-X190 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36',
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; rv:59.0) Gecko/20100101 Firefox/1CB4',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; LG-X190 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.2.2; Vodafone 785 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 8.0; es-LA; SM-G955F Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.8.820 U3/0.8.0 Mobile Safari/534.30',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D100 Safari Line/8.4.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2; Tablet PC 2.0; Microsoft Outlook 15.0.5007; Microsoft Outlook 15.0.5007; ms-office; MSOffice 15)',
        'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; .NET4.0C; .NET4.0E; ms-office; MSOffice 15)',
        'Mozilla/5.0 (Linux; Android 7.1.1; SM-J510FN Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 GSA/7.12.24.21.arm',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Mattermost/3.7.1 Chrome/56.0.2924.87 Electron/1.6.11 Safari/537.36',
        'Microsoft Office/16.0 (Microsoft Outlook Mail 16.0.6568; Pro)',
        'Mozilla/5.0 (Linux; Android 5.1.1; ZUK Z1 Build/LMY49J; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 GSA/7.23.26.21.arm',
        'AndroidDownloadManager/5.1.1 (Linux; U; Android 5.1.1; ZUK Z1 Build/LMY49J)',
        'Mozilla/5.0 (Linux; Android 7.0; SM-A710F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36 GSA/7.17.28.21.arm',
        'Opera/9.80 (Android; Opera Mini/7.5.35721/90.169; U; en) Presto/2.12.423 Version/12.16',
        'Opera/9.80 (J2ME/MIDP; Opera Mini/4.5.40312/90.169; U; id) Presto/2.12.423 Version/12.16',
        'Opera/9.80 (Android; Opera Mini/7.6.40077/90.169; U; en) Presto/2.12.423 Version/12.16',
        'Mozilla/5.0 (Linux; Android 4.4.4; D2203 Build/18.5.C.0.19) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 GSA/7.17.28.16.arm',
        'Mozilla/5.0 (Linux; U; Android 7.0; en-US; E2 Noir Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.1.1108 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/76918C',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.5.2564.88 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12 ( .NET CLR 3.5.30729)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) GSA/39.0.175034278 Mobile/15A432 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 7.0; SM-J330F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36 GSA/7.6.17.21.arm',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A456 [FBAN/FBIOS;FBAV/165.0.0.74.96;FBBV/100174821;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/10.0.2;FBSS/2;FBCR/TDC;FBID/phone;FBLC/da_DK;FBOP/5;FBRV/100174821]',
        'Mozilla/5.0 (Linux; Android 6.0; Lenovo A2016a40 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 GSA/7.7.18.21.arm',
        'Mozilla/5.0 (Windows NT 6.1; rv:59.0) Gecko/20100101 Firefox/1CB4',
    ]

    useragent = random.choice(user_agent_list)
    return useragent


def get_useragent_header():
    """Generates a Header to use in requests.
    :returns dict headers - dict of header"""
    headers = {"user-agent": get_useragent()}
    return headers
