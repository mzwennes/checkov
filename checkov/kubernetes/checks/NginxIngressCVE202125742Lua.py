from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.common.util.data_structures_utils import find_in_dict
from checkov.kubernetes.base_spec_check import BaseK8Check
from checkov.common.util.type_forcers import force_list
import re


class NginxIngressCVE202125742Lua(BaseK8Check):

    def __init__(self):
        name = "Prevent NGINX Ingress annotation snippets which contain LUA code execution. See CVE-2021-25742"
        id = "CKV_K8S_152"
        supported_kind = ['Ingress']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def get_resource_id(self, conf):
        if "namespace" in conf["metadata"]:
            return "{}.{}.{}".format(conf["kind"], conf["metadata"]["name"], conf["metadata"]["namespace"])
        else:
            return "{}.{}.default".format(conf["kind"], conf["metadata"]["name"])

    def scan_spec_conf(self, conf):
        badInjectionPatterns = "\\blua_|_lua\\b|_lua_|\\bkubernetes\\.io\\b"

        if conf["metadata"]:
            if conf["metadata"].get('annotations'):
                for annotation in force_list(conf["metadata"]["annotations"]):
                    for key, value in annotation.items():
                        if "snippet" in key and  re.match(badInjectionPatterns, value):
                            return CheckResult.FAILED
        return CheckResult.PASSED

check = NginxIngressCVE202125742Lua()
