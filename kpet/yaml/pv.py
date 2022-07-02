from attrs import define

from ._node import Node


@define
class PersistentVolume(Node):
    name: str
    accessModes: list[str]
    capacity: str
    storageClassName: str = ""
    hostPath: tuple[str, str] = None
    yaml = """\
apiVersion: v1
kind: PersistentVolume
metadata:
    name: {name}
spec:
    accessModes: {accessModes}
    capacity:
        storage: {capacity}
"""

    def render(self):
        extra_yaml = None
        if self.storageClassName:
            extra_yaml = f"    storageClassName: {self.storageClassName}\n"
        render_txt = super().render(extra_yaml)
        if self.hostPath:
            extra_yaml = f"    hostPath:\n        path: {self.hostPath[0]}\n"
        render_txt = super().render(extra_yaml)
        return "---\n" + render_txt


@define
class Volume(Node):
    name: str
    emptyDir: bool = False
    yaml = """
    -   name: {name}
"""

    def render(self):
        render_txt = super().render()
        if self.emptyDir:
            render_txt += "        emptyDir: {}"
        return render_txt


@define
class VolumeMount(Node):
    volume: Volume
    mountPath: str
