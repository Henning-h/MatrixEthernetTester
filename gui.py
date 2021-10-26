import PySimpleGUI as sg
import paramiko, time, threading

def server_c1(interface):
    if interface == "wlan":
        return '10.0.10.230'
    elif interface == "ethernet":
        return '192.168.88.230'
    else:
        return
    
def client_c1(interface):
    if interface == "wlan":
        return '10.0.10.233'
    elif interface == "ethernet":
        return '192.168.88.233'
    else:
        return
    
def server_c2(interface):
    if interface == "wlan":
        return '10.0.10.231'
    elif interface == "ethernet":
        return '192.168.88.231'
    else:
        return
    
def client_c2(interface):
    if interface == "wlan":
        return '10.0.10.234'
    elif interface == "ethernet":
        return '192.168.88.234'
    else:
        return

def server_c3(interface):
    if interface == "wlan":
        return '10.0.10.232'
    elif interface == "ethernet":
        return '192.168.88.232'
    else:
        return
    
def client_c3_1(interface):
    if interface == "wlan":
        return '10.0.10.235'
    elif interface == "ethernet":
        return '192.168.88.235'
    else:
        return

def client_c3_2(interface):
    if interface == "wlan":
        return '10.0.10.236'
    elif interface == "ethernet":
        return '192.168.88.236'
    else:
        return

def client_c9(interface):
    if interface == "wlan":
        return '10.0.10.237'
    elif interface == "ethernet":
        return '192.168.88.237'
    else:
        return



def set_ips():
    rpi = [server_c1("wlan"),server_c2("wlan"),server_c3("wlan"),client_c1("wlan"),
           client_c2("wlan"),client_c3_1("wlan"),client_c3_2("wlan"),client_c9("wlan")]
    i=0
    global test_running
    while i<len(rpi):
        try:
            print("Setting up IPs on RPI " + rpi[i])
            run_ssh_command(rpi[i],"python usr/src/app/set_eth_ip-py &")
            i = i+1
        except:
            print("Failed to connect to " + rpi[i])
            break
    if i==len(rpi):
        print("Done! Ready for testing")
        print("\n")
        
        test_running = False
    else:
        print("Setting up IPs FAILED!!! No testing possible")
    
 


layout = [
    [sg.Text('Matrix Ethernet Tester', font=('Helvetica', 24, 'bold'))],
    [sg.Button('Run Matrix MKII+ Test'),sg.Button('Run miniMatrix Test') ],
    [sg.Text('Individual tests', font=('Helvetica', 12, 'bold'))],
    [sg.Button('Test C1'), sg.Button('Test C2'), sg.Button('Test C3_1'), sg.Button('Test C3_2'), sg.Button('Test C9')],    
    [sg.Output(key='-OUT-', size=(100, 25))],
]

window = sg.Window('Matrix Ethernet Tester 1.0 by HHH 26.10.2021', layout, element_justification='center').finalize()
window['-OUT-'].TKOut.output.config(wrap='word') # set Output element word wrapping




def run_ssh_command(client_ip,command): #Connect to client IP and run a iPerf towards the server IP
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(client_ip, username="innova", password="innova")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    ssh.close()



def run_iperf(client_ip,server_ip): #Connect to client IP and run a iPerf towards the server IP
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print(client_ip)
    #print(server_ip)
    ssh.connect(client_ip, username="innova", password="innova")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("iperf3 -c " + server_ip + " --json > results.json &" )
    #lines = ssh_stdout.read().decode('ascii').strip("\n")
    #print(lines)
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("exit")
    ssh.close()
    #print("done")
    
   
def get_results(client_ip, server_name, reset_test_running):
    global test_running
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Getting results from " + server_name )
    resultsReady = False
    hasPrinted = False
    while(not resultsReady):
        ssh2.connect(client_ip, username="innova", password="innova")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh2.exec_command("python /usr/src/app/readJSON.py")
        lines = ssh_stdout.read().decode('ascii').strip("\n")
        if lines == "Results are not ready":
            if hasPrinted:
                pass
            else:
                print("Waiting for results")
                hasPrinted = True 
            time.sleep(1)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh2.exec_command("exit")
            ssh2.close()
        else:
            #print("results ready")
            done = True
            resultsReady = True
            print(lines)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh2.exec_command("rm -f results.json")
            lines = ssh_stdout.readlines()
            print("\n")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh2.exec_command("exit")
            ssh2.close()
    if reset_test_running:
        test_running = False
    
    
def test_c1():
    print("Starting iPerf client on server_c1 --> client_c1")
    run_iperf(server_c1("wlan"),client_c1("ethernet"))
   #get_results()
    
def test_c2():
    print("Starting iPerf client on server_c2 --> client_c2") 
    run_iperf(server_c2("wlan"),client_c2("ethernet"))
    #get_results(servers[2][2])

def test_c3_1():
    print("Starting iPerf client on server_c3 --> client_c3_1")
    run_iperf(server_c3("wlan"),client_c3_1("ethernet"))
    #get_results()

def test_c3_2():
    print("Starting iPerf client on client_c3_2 --> server_c3")
    run_iperf(client_c3_2("wlan"),server_c3("ethernet"))
    #get_results()

def test_c9():
    print("Starting iPerf client on  client_c9 --> server_c3")
    run_iperf(client_c9("wlan"),server_c3("ethernet"))
    #get_results()

def mkII_test():

    print("STARTING MATRIX MKII+ TEST")
    test_c1()
    test_c2()
    test_c3_1()
    test_c3_2()
    print("\n")
    print("GETTING RESULTS")
    get_results(server_c1("wlan"), "C1", False)
    get_results(server_c2("wlan"), "C2", False)
    get_results(server_c3("wlan"), "C3_1", False)
    get_results(client_c3_2("wlan"), "C3_2", False)
    test_c9()
    get_results(client_c9("wlan"), "C9", True)

def miniMatrix_test():
    print("STARTING MINIMATRIX TEST")
    test_c1()
    test_c2()
    test_c3_1()
    print("\n")
    print("GETTING RESULTS")
    get_results(server_c1("wlan"), "server_c1", False)
    get_results(server_c2("wlan"), "server_c2", False)
    get_results(server_c3("wlan"), "server_c3", True)

    
test_running = True
set_ips_thread = threading.Thread(target=set_ips)
set_ips_thread.start()

while True:
    event, values = window.read()
    if (event == "Run Matrix MKII+ Test" or event == "Run miniMatrix Test" or event == "Test C1" or event == "Test C2" or event == "Test C3_1" or event == "Test C3_2" or event == "Test C9") and test_running:
        sg.popup('Testing already in progress')
    elif event == "Run Matrix MKII+ Test":
        test_running = True
        Matrix_test_thread = threading.Thread(target=mkII_test)
        Matrix_test_thread.start()
    elif event == "Run miniMatrix Test":
        test_running = True
        miniMatrix_test_thread = threading.Thread(target=miniMatrix_test)
        miniMatrix_test_thread.start()        
    elif event == "Test C1":
        test_running = True
        test_c1()
        get_results_c1_thread = threading.Thread(target=get_results, args=[server_c1("wlan"), "server_c1", True])
        get_results_c1_thread.start()
    elif event == "Test C2":
        test_running = True
        test_c2()
        get_results_c2_thread = threading.Thread(target=get_results, args=[server_c2("wlan"), "server_c2", True])
        get_results_c2_thread.start()
    elif event == "Test C3_1":
        test_running = True
        test_c3_1()
        get_results_c3_thread = threading.Thread(target=get_results, args=[server_c3("wlan"), "server_c3", True])
        get_results_c3_thread.start()
    elif event == "Test C3_2":
        test_running = True
        test_c3_2()
        get_results_c3_2_thread = threading.Thread(target=get_results, args=[client_c3_2("wlan"), "client_c3_2", True])
        get_results_c3_2_thread.start()
    elif event == "Test C9":
        test_running = True
        test_c9()
        get_results_c9_thread = threading.Thread(target=get_results, args=[client_c9("wlan"), "client_c9", True])
        get_results_c9_thread.start()
        
    elif event == sg.WIN_CLOSED:
        break

window.close()
