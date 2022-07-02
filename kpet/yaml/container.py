from attrs import define

from ._node import Node


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
            render_txt += (
                "\n".join([f"          - {repr(arg)}" for arg in self.args]) + "\n"
            )
        return render_txt
