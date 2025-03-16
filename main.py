#Alunos: Dionatas e Meilen

import matplotlib.pyplot as plt
import numpy as np
import cv2
import json
from cv2 import aruco
from matplotlib.lines import Line2D



print('##########################################################################################################################')
print("[LOG]: Carregando os Parametros das cameras")

def camera_parameters(file):
    camera_data = json.load(open(file))
    K = np.array(camera_data['intrinsic']['doubles']).reshape(3, 3)
    res = [camera_data['resolution']['width'],
        camera_data['resolution']['height']]
    tf = np.array(camera_data['extrinsic']['tf']['doubles']).reshape(4, 4)
    R = tf[:3, :3]
    T = tf[:3, 3].reshape(3, 1)
    dis = np.array(camera_data['distortion']['doubles'])
    T = np.dot(-R.T,T)
    R = R.T
    return K, R, T, res, dis

K0, R0, T0, resolucao0, distorcao0 = camera_parameters('./assets/json/0.json')
K1, R1, T1, resolucao1, distorcao1 = camera_parameters('./assets/json/1.json')
K2, R2, T2, resolucao2, distorcao2 = camera_parameters('./assets/json/2.json')
K3, R3, T3, resolucao3, distorcao3 = camera_parameters('./assets/json/3.json')

def print_camera_parameters(K, R, T, resolucao, distorcao, index):
    print(    f"\n\n->Camera {index}:")
    print(    f"    K (Matriz Intrinseca):\n{K}")
    print(    f"    R (Matriz de Rotacao):\n{R}")
    print(    f"    T (Vetor de Translacao):\n{T}")
    print(    f"    Resolucao: {resolucao}")
    print(    f"    Distorcao: {distorcao}\n")

K0, R0, T0, resolucao0, distorcao0 = camera_parameters('./assets/json/0.json')
K1, R1, T1, resolucao1, distorcao1 = camera_parameters('./assets/json/1.json')
K2, R2, T2, resolucao2, distorcao2 = camera_parameters('./assets/json/2.json')
K3, R3, T3, resolucao3, distorcao3 = camera_parameters('./assets/json/3.json')

print_camera_parameters(K0, R0, T0, resolucao0, distorcao0, 0)
print_camera_parameters(K1, R1, T1, resolucao1, distorcao1, 1)
print_camera_parameters(K2, R2, T2, resolucao2, distorcao2, 2)
print_camera_parameters(K3, R3, T3, resolucao3, distorcao3, 3)
print("[LOG]: Parametros das cameras carregados com sucesso")


# print('##########################################################################################################################')
# print("[LOG]: Lendo os arquivos de video")
# read_video0 = "./assets/video/camera-00.mp4"
# read_video1 = "./assets/video/camera-01.mp4"
# read_video2 = "./assets/video/camera-02.mp4"
# read_video3 = "./assets/video/camera-03.mp4"
# print("[LOG]: Arquivos de video lidos com sucesso")


print('##########################################################################################################################')
print("[LOG]: Lendo os arquivos de video")
camera0 = cv2.VideoCapture("./assets/video/camera-00.mp4")
camera1 = cv2.VideoCapture("./assets/video/camera-01.mp4")
camera2 = cv2.VideoCapture("./assets/video/camera-02.mp4")
camera3 = cv2.VideoCapture("./assets/video/camera-03.mp4")
print("[LOG]: Arquivos de video lidos com sucesso")

print('##########################################################################################################################')
print("[LOG]: Subindo os parametros do aruco")
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
print("[LOG]: Parametros do aruco subidos com sucesso")


print('##########################################################################################################################')
print("[LOG]: Criando vetores para armazenar as coordinates e o numero de cameras")
robot_coordinates = []
number_cameras = []

print("[LOG]: Iniciando a leitura dos videos")
while True:
    ret0, img0 = camera0.read()
    ret1, img1 = camera1.read()
    ret2, img2 = camera2.read()
    ret3, img3 = camera3.read()

    if not ret0 or not ret1 or not ret2 or not ret3:
        print("[LOG]: Falha na captura de alguma câmera")
        break
    if img0 is None or img1 is None or img2 is None or img3 is None:
        print("[LOG]: Empty Frame")
        break
    print("[LOG]: Transformando a imagem para tons de cinza")
    gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    
    print("[LOG]: Criando o objeto aruco")
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    print("[LOG]: Detectando os marcadores na imagem")
    corners0, ids0, rejectedImgPoints = detector.detectMarkers(gray0)
    corners1, ids1, rejectedImgPoints = detector.detectMarkers(gray1)
    corners2, ids2, rejectedImgPoints = detector.detectMarkers(gray2)
    corners3, ids3, rejectedImgPoints = detector.detectMarkers(gray3)

    print("[LOG]: Filtrando os arucos (para pegar apenas o que esta no robo (id = 0))")
    if ids0 is not None:
        corners0_filtered = []
        ids0_filtered = None
        for i in range(0, len(ids0)):
            if ids0[i] == 0:                
                corners0_filtered = [corners0[i]]
                ids0_filtered = ids0[i]
    else:
        corners0_filtered = corners0
        ids0_filtered = ids0  
    if ids1 is not None:
        corners1_filtered = []
        ids1_filtered = None
        for i in range(0, len(ids1)):
            if ids1[i] == 0:                
                corners1_filtered = [corners1[i]]
                ids1_filtered = ids1[i]
    else:
        corners1_filtered = corners1
        ids1_filtered = ids1
    if ids2 is not None:
        corners2_filtered = []
        ids2_filtered = None
        for i in range(0, len(ids2)):
            if ids2[i] == 0:                
                corners2_filtered = [corners2[i]]
                ids2_filtered = ids2[i]
    else:
        corners2_filtered = corners2
        ids2_filtered = ids2

    if ids3 is not None:
        corners3_filtered = []
        ids3_filtered = None
        for i in range(0, len(ids3)):
            if ids3[i] == 0:                
                corners3_filtered = [corners3[i]]
                ids3_filtered = ids3[i]
    else:
        corners3_filtered = corners3
        ids3_filtered = ids3

    print("[LOG]: Marcando os marcadores na imagem")
    frame_markers0 = aruco.drawDetectedMarkers(img0.copy(), corners0_filtered, ids0_filtered)
    frame_markers1 = aruco.drawDetectedMarkers(img1.copy(), corners1_filtered, ids1_filtered)
    frame_markers2 = aruco.drawDetectedMarkers(img2.copy(), corners2_filtered, ids2_filtered)
    frame_markers3 = aruco.drawDetectedMarkers(img3.copy(), corners3_filtered, ids3_filtered)
    cv2.putText(frame_markers0, "Camera 0", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(frame_markers1, "Camera 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(frame_markers2, "Camera 2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(frame_markers3, "Camera 3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_AA)


    print("[LOG]: Juntando os 4 videos para aparecerem na mesma janela")
    stack01 = np.vstack((frame_markers0,frame_markers1))
    stack23 = np.vstack((frame_markers2,frame_markers3))
    stack_all = np.hstack((stack01,stack23))

    cv2.imshow('Os quatro videos com robo + aruco',cv2.resize(stack_all, resolucao0))

    print("[LOG]: Verificando em quantas cameras foram identificados os arucos do robo e quais sao elas")
    count_camera = 0
    flag_camera = []

    if corners0_filtered == ():
        flag_camera.append(0)
        pass
    else:
        count_camera = count_camera + 1
        flag_camera.append(1)

    if corners1_filtered == []:
        flag_camera.append(0)
        pass
    else:
        count_camera = count_camera + 1
        flag_camera.append(1)

    if corners2_filtered == ():
        flag_camera.append(0)
        pass
    else:
        count_camera = count_camera + 1
        flag_camera.append(1)
    
    if corners3_filtered == ():
        flag_camera.append(0)
        pass
    else:
        count_camera = count_camera + 1
        flag_camera.append(1)

    print("[LOG]: Montando a matriz A e RT")
    if count_camera < 2:
        print('Cameras insuficientes')

    else:
        A = np.zeros((3*count_camera, count_camera+3))
        RT = np.zeros((3*count_camera,1))
        aux = 0
        print("[LOG]: Preenchendo a matriz A e RT")
        for i in range(0,1):
            if flag_camera[0] == 1:
                A[3*aux:(aux+1)*3, 0:3] = -np.identity(3)
                central_point0 = np.mean(corners0_filtered[0][0], axis = 0) 
                central_point0 = np.concatenate((central_point0,[1]))
                A[3*aux:(aux+1)*3, aux + 3] = np.dot(np.linalg.inv(np.dot(K0,R0)), central_point0)
                RT[3*aux:(aux+1)*3] = np.dot(np.linalg.inv(R0),T0)
                aux = aux + 1

            if aux >= count_camera:
                break
            
            if flag_camera[1] == 1:
                A[3*aux:(aux+1)*3, 0:3] = -np.identity(3)
                central_point1 = np.mean(corners1_filtered[0][0], axis = 0) 
                central_point1 = np.concatenate((central_point1,[1]))
                A[3*aux:(aux+1)*3, aux + 3] = np.dot(np.linalg.inv(np.dot(K1,R1)), central_point1)
                RT[3*aux:(aux+1)*3] = np.dot(np.linalg.inv(R1),T1)
                aux = aux + 1
            
            if aux >= count_camera:
                break

            if flag_camera[2] == 1:
                A[3*aux:(aux+1)*3, 0:3] = -np.identity(3)
                central_point2 = np.mean(corners2_filtered[0][0], axis = 0) 
                central_point2 = np.concatenate((central_point2,[1]))
                A[3*aux:(aux+1)*3, aux + 3] = np.dot(np.linalg.inv(np.dot(K2,R2)), central_point2)
                RT[3*aux:(aux+1)*3] = np.dot(np.linalg.inv(R2),T2)
                aux = aux + 1

            if aux >= count_camera:
                break

            if flag_camera[3] == 1:
                A[3*aux:(aux+1)*3, 0:3] = -np.identity(3)
                central_point3 = np.mean(corners3_filtered[0][0], axis = 0) 
                central_point3 = np.concatenate((central_point3,[1]))
                A[3*aux:(aux+1)*3, aux + 3] = np.dot(np.linalg.inv(np.dot(K3,R3)), central_point3)
                RT[3*aux:(aux+1)*3] = np.dot(np.linalg.inv(R3),T3)
                aux = aux + 1
            
            if aux >= count_camera:
                break
        print("[LOG]: Resolvendo a equacao das matrizes para obter a coordenada")
        A_pseudo = np.linalg.pinv(A)
        eq = np.dot(A_pseudo, RT)
        robot_coordinates.append(eq[0:3])
        print("[LOG]: Salvando o numero de cameras")
        number_cameras.append(count_camera)    

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
print("[LOG]: Finalizando a leitura dos videos")

print('##########################################################################################################################')
print("[LOG]: Separando as coordinates do robo em uma lista pra cada eixo")
robot_coordinates = np.array(robot_coordinates)
coordinates_x = (robot_coordinates[:,0])
coordinates_x = list(np.concatenate(coordinates_x).flat)

coordinates_y = (robot_coordinates[:,1])
coordinates_y = list(np.concatenate(coordinates_y).flat)

coordinates_z = (robot_coordinates[:,2])
coordinates_z = list(np.concatenate(coordinates_z).flat)

cx_2cam = []
cy_2cam = []
cz_2cam = []

cx_3cam = []
cy_3cam = []
cz_3cam = []

cx_4cam = []
cy_4cam = []
cz_4cam = []

print("[LOG]: Separando as coordinates do robo de acordo com o numero de cameras que realizaram a identificacao")
for i in range(0,len(number_cameras)):
    if number_cameras[i] == 2:
        cx_2cam.append(coordinates_x[i])
        cy_2cam.append(coordinates_y[i])
        cz_2cam.append(coordinates_z[i])

    elif number_cameras[i] == 3:
        cx_3cam.append(coordinates_x[i])
        cy_3cam.append(coordinates_y[i])
        cz_3cam.append(coordinates_z[i])

    elif number_cameras[i] == 4:
        cx_4cam.append(coordinates_x[i])
        cy_4cam.append(coordinates_y[i])
        cz_4cam.append(coordinates_z[i])

print("[LOG]: Plotando a reconstrucao do movimento do robo")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)


print("[LOG]: Plotando a rota do robo")

r1 = ax1.scatter(xs = coordinates_x[0], ys = coordinates_y[0], zs = coordinates_z[0], 
                c = "yellow", label = 'Início da Rota', s = 600, marker= "^")  
r2 = ax1.scatter(xs = coordinates_x[1:], ys = coordinates_y[1:], zs = coordinates_z[1:], 
                c = "black", label = 'Rota Robo')
r3 = ax1.scatter(xs = coordinates_x[-1], ys = coordinates_y[-1], zs = coordinates_z[-1], 
                c = "red", label = 'Fim da Rota', s = 600, marker= "^")  
legend_start = Line2D([0], [0], marker='^', color='w', markerfacecolor='yellow', markersize=10, label='Início da Rota')
legend_end = Line2D([0], [0], marker='^', color='w', markerfacecolor='red', markersize=10, label='Fim da Rota')

# Adicionando à legenda
ax1.legend(handles=[legend_start, legend_end, r2])
ax1.set_xlabel("X (m)")
ax1.set_ylabel("Y (m)")
ax1.set_zlabel("Z (m)")
ax1.set_xlim([-1.8,1.8])
ax1.set_ylim([-0.75,0.75])
ax1.set_zlim([0,1])
ax1.view_init(elev=35,azim=-90)
ax1.set_title("Reconstrucao do Movimento do Robô Móvel")

print("[LOG]: Plotando as cameras que identificaram o robo")
c1 = ax2.scatter(x = cx_2cam, y = cy_2cam,  c = "red",label = 'Movimento identificado por duas cameras')
c2 = ax2.scatter(x = cx_3cam, y = cy_3cam,  c = "green",label = 'Movimento identificado por três cameras')
c3 = ax2.scatter(x = cx_4cam, y = cy_4cam,  c = "blue",label = 'Movimento identificado por quatro cameras')
ax2.legend()
ax2.grid(True)
ax2.set_xlabel("X (m)")
ax2.set_ylabel("Y (m)")
ax2.set_title("Cameras que Identificaram o Robô", fontsize=12)
plt.tight_layout()
plt.show()
print("[LOG]: Reconstrucao do movimento do robo finalizada com sucesso")
print('##########################################################################################################################')
