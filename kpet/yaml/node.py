from dinterpol import Template
from rich import print
from rich.syntax import Syntax

frame = []
parent = None


class Node:
    def __enter__(self):
        global parent
        self.childs = []
        frame.append(self)
        if parent:
            parent.childs.append(self)
        parent = self
        return self

    def __exit__(self, type, value, traceback):
        frame.pop()

    def render(self):
        return Template(self.yaml).render(self.__members__)

    def print(self):
        yaml = Syntax(self.render(), "yaml")
        print(yaml)

    def render_childs(self, child_type: type):
        render_txt = ""
        """render all childs which are instances of child_type"""
        for child in self.childs:
            if isinstance(child, child_type):
                render_txt += child.render()
        return render_txt

    @property
    def __members__(self):
        member_dict = {}
        for name in dir(self):
            if not name.startswith("__"):
                member_dict[name] = getattr(self, name)
        return member_dict
