import os

def setup_ifb(interface):
    os.system("modprobe ifb")
    os.system(f"tc qdisc add dev {interface} ingress")
    os.system(f"tc filter add dev {interface} parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0")
    os.system("ip link set ifb0 up")
    print(f"IFB interface setup complete for {interface}")
