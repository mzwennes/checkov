from bridgecrew.terraformscanner.models.enums import ScanResult, ScanCategories
from bridgecrew.terraformscanner.resource_scanner import ResourceScanner


class PasswordPolicyUppcaseLetter(ResourceScanner):
    def __init__(self):
        name = "Ensure IAM password policy requires at least one uppercase letter"
        scan_id = "BC_AWS_IAM_5"
        supported_resources = ['aws_iam_account_password_policy']
        categories = [ScanCategories.IAM]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            validates iam password policy
            https://www.terraform.io/docs/providers/aws/r/iam_account_password_policy.html
        :param conf: aws_iam_account_password_policy configuration
        :return: <ScanResult>
        """
        key = 'require_uppercase_characters'
        if key in conf.keys():
            if conf[key]:
                return ScanResult.SUCCESS
        return ScanResult.FAILURE


scanner = PasswordPolicyUppcaseLetter()
