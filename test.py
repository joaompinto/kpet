from kpet.yaml import Container, PersistentVolume, Pod

pv = PersistentVolume("test", ["ReadWriteOnce"], "10Gi", hostPath=("/data", ""))
with Pod("busybox-sleep") as pod:
    Container("busybox", "busybox:1.28", args=["sleep", "100000"]).add()
    Container("busybox2", "busybox:1.20", args=["sleep", "100000"]).add()

pv.print()
pod.print()
