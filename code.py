from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session
from dotenv import load_dotenv
import os

# Définition des constantes
BACKEND_NAME = "ibm_brisbane"
OPTIMIZATION_LEVEL = 3

# Récupération du token d'API depuis le fichier d'environnement
load_dotenv()
api_token = os.getenv("IBM_API_TOKEN")
if api_token is None:
    print("Erreur: IBM_API_TOKEN manquant dans le fichier .env")
    exit(1)

# Connexion au service IBM Quantum
try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=api_token)
    backend = service.backend(BACKEND_NAME)
except Exception as e:
    print(f"Erreur de connexion à IBM Quantum: {e}")
    exit(1)

# Création du circuit quantique
circuit = QuantumCircuit(2)
circuit.h(0)           # Application d'une porte Hadamard sur le qubit 0
circuit.cx(0, 1)       # Application d'une porte CNOT entre les qubits 0 et 1
circuit.measure_all()  # Mesure de tous les qubits

# Optimisation du circuit pour le backend cible
try:
    optimized_circuit = transpile(circuit, backend=backend, optimization_level=OPTIMIZATION_LEVEL)
except Exception as e:
    print(f"Erreur lors de la transpilation: {e}")
    exit(1)

# Exécution du circuit sur le backend
try:
    with Session(backend=backend) as session:
        sampler = Sampler(mode=session)
        job = sampler.run([optimized_circuit])
        print(f"Job ID: {job.job_id()}")
except Exception as e:
    print(f"Erreur lors de l'exécution du circuit: {e}")
    exit(1)
