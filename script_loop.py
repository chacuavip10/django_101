import ipaddress
ldif = ""
# Input from user
d = "y"
while d == "y":
    uid = input("Username/UID: ")
    password = input("Password(1 to user default 1a2b3c4d): ")
    if str(password) == "1":
        print("Password default to: 1a2b3c4d")
        password = "1a2b3c4d"
    # print(f"Username: {uid}\nPassword: {password}")
    list_goi_cuoc = {1: "CN1", 2: "CN2",
                     3: "CN3", 4: "CN4", 5: "CN5", 6: "CN6"}
    cust_type = {0: "IP dong/CGNAT", 1: "IP tinh",
                 2: "IP tinh, 1 block ip", 3: "IP tinh, 2 block ip"}
    # Lay thong tin goi cuoc
    goi_cuoc = 8
    while (int(goi_cuoc) >= 7) or (int(goi_cuoc) <= 0):
        print("Lua chon goi cuoc(1-6): ")
        for x in list_goi_cuoc:
            print(f"{x}: {list_goi_cuoc[x]}")
        goi_cuoc = int(
            input("=================>: "))
    goi_cuoc_name = list_goi_cuoc.get(goi_cuoc)
    # Lay thong tin  k/h ip tinh, ip dong
    kh = 8
    while (int(kh) >= 7) or (int(kh) < 0):
        print("Lua chon goi cuoc(1-3): ")
        for x in cust_type:
            print((f"{x}: {cust_type[x]}"))
        kh = int(input("=================>: "))
    cust_type_name = cust_type.get(kh)
    if kh >= 1:
        test = True
        while test == True:
            try:
                IP_Static = input(
                    "Dia chi Ip tinh: ")
                if ipaddress.ip_address(IP_Static).is_private == True:
                    test = True
                    print("Dia chi ip la private, moi nhap lai dia chi public!")
                else:
                    test = False
            except ValueError:
                print("Sai cu phap dia chi ip! (x.x.x.x, x <= 255)")
    if kh >= 2:
        # Input block ip
        test = True
        while test == True:
            try:
                Framed_Route_1 = ipaddress.ip_network(
                    input("Block IP, subnetmask default /32: "))
                if ipaddress.ip_network(Framed_Route_1).is_private == True:
                    test = True
                    print("Dai dia chi ip la private, moi nhap lai dai dia chi public!")
                else:
                    test = False
            except ValueError:
                print("Sai cu phap block ip! (ipaddress/subnetmask)")
    if kh >= 3:
        # Input block ip 2
        test = True
        while test == True:
            try:
                Framed_Route_2 = ipaddress.ip_network(
                    input("Block IP 2, subnetmask default /32: "))
                if ipaddress.ip_network(Framed_Route_1).is_private == True:
                    test = True
                    print("Dai dia chi ip la private, moi nhap lai dai dia chi public!")
                else:
                    test = False
            except ValueError:
                print("Sai cu phap block ip! (ipaddress/subnetmask)")
    print(
        f"Username: {uid}\nPassword: {password}\nGoi cuoc: {goi_cuoc_name}\nKH: {cust_type_name}")
    # Kiem tra xem co dua kh vao group cn ko, hien tai cn ho tro tu 1 - 6
    if 1 <= int(goi_cuoc) <= 6:
        ldif = ldif + "dn: uid=" + str(uid) + ",cn=" + str(goi_cuoc_name)
    else:
        ldif = ldif + "dn: uid=" + str(uid)
    ldif = ldif + ",ou=hni,dc=mobifone,dc=vn" + """\nchangetype: add
objectClass: top
objectClass: person
objectClass: organizationalperson
objectClass: inetorgperson
objectClass: ftth-postpaid""" + "\ngivenname: " + str(uid) + "\nsn: " + str(uid) + "\nuid: " + str(uid) + "\ncn: " + str(uid) + "\nuserPassword: " + str(password)
    # Add attribute goi cuoc ipv4
    ldif = ldif + "\nJnpr-IPv6-Ingress-Policy-Name: ipv6-U-" + \
        str(goi_cuoc_name) + "\nJnpr-IPv6-Egress-Policy-Name: ipv6-D-" + \
        str(goi_cuoc_name)
    # Add atrribute goi cuoc ipv6
    ldif = ldif + "\nUnisphere-Ingress-Policy-Name: U-" + \
        str(goi_cuoc_name) + "\nUnisphere-Egress-Policy-Name: D-" + \
        str(goi_cuoc_name)
    if kh == 0:
        ldif = ldif + """\nFramed-Pool: ftth_private
Framed-IPv6-Pool: FTTH-V6-WAN-CGNAT
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN-CGNAT
Unisphere-Virtual-Router: VRF_CGNAT"""
    if kh >= 1:
        ldif = ldif + "\nFramed-Ip-Address: " + \
            str(IP_Static) + "\nFramed-IP-Netmask: 255.255.255.255"
    if kh >= 2:
        ldif = ldif + "\nFramed-Route: " + str(Framed_Route_1)
    if kh >= 3:
        ldif = ldif + "\nFramed-Route: " + str(Framed_Route_2)
    if kh >= 1:
        ldif = ldif + """\nFramed-IPv6-Pool: FTTH-V6-WAN
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN"""
    ldif = ldif + "\n\n"
    d = input("Them khach hang? (choose y for yes, any other keys for no): ")
print("==================================================")
# print(ldif)
# Strip new line at the end of tring
ldif = ldif.rstrip()
print(ldif)
# Write to file
f = open("add_new_user.ldif", "w")
f.write(ldif)
f.close()
