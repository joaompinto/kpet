from attrs import define

from .node import Node


@define
class Pod(Node):
    name: str
    yaml = """\
apiVersion: v1
kind: Pod
metadata:
    name: {name}
spec:
    containers:"""

    def render(self):
        render_txt = super().render()
        render_txt += self.render_childs(Container)
        return render_txt


@define
class Container(Node):
    name: str
    image: str
    args: list = []
    yaml = """
    -   name: {name}
        image: {image}
"""

    def render(self):
        render_txt = super().render()
        if self.args:
            render_txt += "        args:\n"
            for arg in self.args:
                render_txt += f"          - {repr(arg)}\n"
        return render_txt
