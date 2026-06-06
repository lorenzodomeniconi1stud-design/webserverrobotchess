import socket
import serial
import time

# --- IMPOSTAZIONI ROBOT ---
ROBOT_IP = "192.168.125.1" 
PORT = 1025

# --- IMPOSTAZIONI ARDUINO ---
# Cambia 'COM3' con la porta corretta (es. 'COM4' su Windows o '/dev/ttyACM0' su Linux/Mac)
SERIAL_PORT = "COM13"
BAUD_RATE = 115200

print("Inizializzazione delle connessioni...")

try:
    # 1. Connessione ad Arduino (Seriale)
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    # Arduino si riavvia spesso quando si apre la seriale, una breve pausa è raccomandata
    time.sleep(2) 
    print(f"Connesso ad ESP32 sulla porta {SERIAL_PORT}!")

    # 2. Connessione al Robot (Socket TCP)
    
    #robot_socket.settimeout(20) # Timeout iniziale per la connessione
    #robot_socket.connect((ROBOT_IP, PORT))
    #print(f"Connesso al robot all'IP {ROBOT_IP} sulla porta {PORT}!")
    
    # Rimuoviamo il timeout stringente ora che siamo connessi, 
    # così il socket non si chiude mentre aspettiamo i dati da Arduino
    #robot_socket.settimeout(None)

    #print("\nIn ascolto su Arduino... (Premi Ctrl+C per interrompere)")

    # 3. Ciclo di lettura e reindirizzamento
    while True:
        # Controlla se ci sono dati in arrivo dalla seriale
        if arduino.in_waiting > 0:
            # Legge la riga da Arduino, la decodifica e rimuove spazi/invio a fine riga
            dati_arduino = arduino.readline().decode('utf-8').strip()
            
            # Se la stringa non è vuota, processala
            if dati_arduino:
                print(f"Ricevuto da Arduino: {dati_arduino}")
                robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                robot_socket.settimeout(20)
                robot_socket.connect((ROBOT_IP, PORT))
                robot_socket.settimeout(None)

                print("\nIn ascolto su Arduino... (Premi Ctrl+C per interrompere)")
                print(f"Connesso al robot all'IP {ROBOT_IP} sulla porta {PORT}!")
                # Converte la stringa in byte per inviarla via socket
                coordinate = dati_arduino.encode('utf-8')
                
                # Invia al robot
                robot_socket.sendall(coordinate)
                print(" -> Inviato al robot con successo.")
                robot_socket.close()

except KeyboardInterrupt:
    # Gestisce l'interruzione manuale da parte dell'utente (Ctrl+C)
    print("\nInterruzione manuale rilevata. Chiusura in corso...")

except Exception as e:
    # Cattura e stampa qualsiasi altro errore di connessione/comunicazione
    print(f"\nErrore imprevisto: {e}")

finally:
    # 4. Chiusura sicura di tutte le porte e connessioni
    try:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("Porta seriale chiusa.")
    except Exception:
        pass

    try:
        if 'robot_socket' in locals():
            robot_socket.close()
            print("Connessione socket chiusa.")
    except Exception:
        pass
    
    print("Programma terminato.")