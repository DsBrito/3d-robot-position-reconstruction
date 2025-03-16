# Reconstrução da Posição 3D de um Robô Móvel

## 📌 Descrição

Este projeto tem como objetivo reconstruir a posição 3D de um robô móvel a partir de vídeos capturados por quatro câmeras no espaço inteligente. Para isso, utilizamos marcadores ArUco e técnicas de visão computacional para identificar a posição do robô em cada quadro dos vídeos e, a partir dessas informações, reconstruir sua trajetória no espaço 3D.

## 🎯 Objetivos

- Detectar o robô nos vídeos das quatro câmeras utilizando um marcador ArUco.
- Obter a reconstrução da posição 3D do robô no mundo.
- Gerar um gráfico que represente a trajetória do robô.

## 🛠️ Metodologia

1. **Detecção do Marcador ArUco**

   - O robô está identificado por um marcador ArUco com **ID = 0** e tamanho **30 x 30 cm**.
   - As imagens capturadas pelas quatro câmeras são processadas para identificar o marcador e obter suas coordenadas na imagem.
   - O código fornecido auxilia na detecção desses marcadores.

2. **Calibração das Câmeras**

   - São fornecidos quatro arquivos `.json` contendo os parâmetros **intrínsecos** e **extrínsecos** de cada câmera.
   - A matriz de rotação **R** e a matriz de translação **T** representam a transformação **do referencial da câmera para o mundo**.
   - Para utilizá-las corretamente no modelo de projeção pinhole, **é necessário inverter essa matriz** para obter a transformação do mundo para a câmera.

3. **Reconstrução da Posição 3D**

   - A partir das coordenadas 2D extraídas de cada câmera e os parâmetros de calibração, a posição 3D do robô é calculada.
   - Métodos de triangulação e transformação geométrica são aplicados para reconstruir a posição no espaço tridimensional.

4. **Geração da Trajetória**
   - A trajetória do robô é gerada e visualizada em um gráfico 3D.
   - O resultado final mostra o deslocamento do robô ao longo do tempo.

## 📂 Estrutura do Projeto

📁 projeto_reconstrucao_3D  
│── 📂 assets/  
│───── 📂 videos/ # Vídeos das 4 câmeras  
│───── 📂 json/ # Arquivos JSON com os parâmetros das câmeras  
│── 📂 src/
│───── 📂 utils/  
│───── detect_markers_video.py # Exemplo de Rotina para detectar o marcador ArUco em video
│─────detect_markers.py # Exemplo de Rotina para detectar o marcador ArUco  
│───── parametros.py # Exemplo de parametros iniciais
│── main.py # Arquivo principal (A ser executado)
│── README.md # Este documento

````

## 📦 Dependências

Para executar este projeto, instale as seguintes bibliotecas:

```bash
pip install opencv-python numpy matplotlib
````

## 🚀 Como Executar

python python .\main.py

```

## 📌 Observações Importantes

- Apenas o **marcador de ID = 0** deve ser considerado.
- As matrizes extrínsecas fornecidas nos arquivos `.json` **devem ser invertidas** antes do uso.
- Os vídeos das câmeras estão **sincronizados** para garantir a consistência da reconstrução.
```
