from dinterpol import Template
from rich import print as rich_print
from rich.syntax import Syntax

stack = []
parent = None


class Node:
    def __enter__(self):
        global stack
        parent = None
        if stack:
            parent = stack[-1]
        self.childs = []
        stack.append(self)
        self.parent = parent
        if parent:
            self.parent.childs.append(self)
        else:
            stack.append(self)
        return self

    def __exit__(self, type, value, traceback):
        global stack
        stack.pop()

    def add(self):
        if stack:
            parent = stack[-1]
            parent.childs.append(self)
        return self

    def render(self, extra_yaml: str = "") -> str:
        members = self.__members__
        txt = Template(self.yaml).render(members)
        if extra_yaml:
            txt += extra_yaml
        return txt

    def print(self):
        yaml = Syntax(self.render(), "yaml")
        rich_print(yaml)

    def render_childs(self, key, child_type: type):
        render_txt = ""
        """render all childs which are instances of child_type """
        for child in self.childs:
            if isinstance(child, child_type):
                render_txt += child.render()
        if render_txt:
            render_txt = f"    {key}:" + render_txt
        return render_txt

    @property
    def __members__(self):
        member_dict = {}
        for name in dir(self):
            if not name.startswith("__"):
                member_dict[name] = getattr(self, name)
        return member_dict
