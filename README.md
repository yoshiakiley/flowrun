# flowrun


```python
from flowrun.flow import FlowRun

flow = FlowRun(
    req_url='http://0.0.0.0:8080', name='flow_name'
)
flow.add_step(
    name='step_name', action='action_name',
    step={'SUCCESS': 'done', 'FAIL': 'done'}, args={'args_1': 'a', 'args_2': 'b'}
)

flow.send_echoer()
```