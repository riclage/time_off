from bamboohr_api import BambooHr
from use_cases import GetQuoteOfTheDayUseCase, AutoApproveRequestsUseCase


def main():
    hr_api = BambooHr('your company id', 'your api key')
    quotes_use_case = GetQuoteOfTheDayUseCase()
    auto_approve_use_case = AutoApproveRequestsUseCase(hr_api, quotes_use_case)

    status_msgs = auto_approve_use_case.auto_approve_requests()
    
    if len(status_msgs) == 0:
        print("Nothing to approve")
    else:
        for msg in status_msgs:
            print(msg)


if __name__ == "__main__":
    main()
