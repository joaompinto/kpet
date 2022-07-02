from kpet.yaml.k8s import Container, Pod

with Pod("busybox-sleep") as pod:
    with Container("busybox", "busybox:1.28", args=["sleep", "100000"]) as container:
        pass

pod.print()
