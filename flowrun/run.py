import traceback
import requests
from utils import error_suppress
from step import Step


def false():
    print('发送 echoer 错误', traceback.format_exc())
    return False


class FlowRun:

    def __init__(self, req_url, name):
        self.req_url = req_url
        self._name = name
        self._step_list = []
        self._desc = []
        self._step = []

    def add_step(self, name, step, action, args):
        new_step = Step(name=name, action=action)
        desc = new_step.flow_return(step=step, args=args)
        self._step = list(set(self._step).union(set(desc)))
        self._step.sort()
        self._step_list.append(new_step)

    def check_desc(self, desc):
        if not set(self._step).issubset(set(desc.keys())):
            return False
        return True

    def generate(self):
        data = ''
        for step in self._step_list:
            _ = step.generate()
            data += f'{_}\n'
        return f'flow_run  {self._name}\n {data} flow_run_end'

    def send_echoer(self):
        a = self.generate()
        a = a.replace('"`', '`')
        a = a.replace('`"', '`')
        flow_data = {'data': a}
        print(flow_data['data'])

        with error_suppress(false):
            req = requests.post(self.req_url, json=flow_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('发送echoer错误', req.json())
                return False


class Action:
    def __init__(self, req_url, name):
        self.name = name
        self.req_url = req_url
        self.params = ''

    def add_data(self, dictData):
        if not isinstance(dictData, dict):
            return False
        length = len(dictData)
        params = '('
        for k, v in dictData.items():
            if str(v) != 'str' and str(v) != 'int':
                return False
            if length == 1:
                params += f'{v} {k})'
            else:
                params += f'{v} {k},'
            length -= 1
        self.params = params
        return True

    def generate(self):
        data = \
            f"""action {self.name}
                  addr = "{self.req_url}";
                  method = http;
                  args = {self.params};
                  return = (SUCCESS | FAIL);
                action_end
            """
        return data

    def send_echoer(self):
        data = self.generate()
        action_data = {"data": data}
        with error_suppress(false):
            req = requests.post(self.req_url, json=action_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('action发送echoer错误', req.json())
                return False
