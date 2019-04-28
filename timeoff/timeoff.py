from bamboohr_api import BambooHr
from use_cases import GetQuoteOfTheDayUseCase, AutoApproveRequestsUseCase, WikiQuoteApi, MailGunEmailApi, \
    ReportAutoApproveResultUseCase


def main():
    hr_api = BambooHr('your company id', 'your api key')
    quotes_use_case = GetQuoteOfTheDayUseCase(WikiQuoteApi())
    auto_approve_use_case = AutoApproveRequestsUseCase(hr_api, quotes_use_case)

    email_api = MailGunEmailApi("your post url", "your api key")
    report_use_case = ReportAutoApproveResultUseCase(email_api)

    status_msgs = auto_approve_use_case.auto_approve_requests()
    report_use_case.report_results(status_msgs)


if __name__ == "__main__":
    main()
