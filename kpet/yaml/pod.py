from attrs import define

from kpet.yaml.pv import Volume

from ._node import Node
from .container import Container


@define
class Pod(Node):
    name: str
    yaml = """\
apiVersion: v1
kind: Pod
metadata:
    name: {name}
spec:
"""

    def render(self):
        render_txt = super().render()
        render_txt += self.render_childs("containers", Container)
        render_txt += self.render_childs("volumes", Volume)
        return "---\n" + render_txt
