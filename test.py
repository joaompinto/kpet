from kpet.yaml import Container, PersistentVolume, Pod, Volume, VolumeMount

pv = PersistentVolume("test", ["ReadWriteOnce"], "10Gi", hostPath=("/data", ""))
with Pod("busybox-sleep") as pod:
    volume = Volume("data-storage", emptyDir=True).add()
    with Container("busybox", "busybox:1.28", args=["sleep", "100000"]):
        VolumeMount(volume, "/data").add()

pv.print()
pod.print()
