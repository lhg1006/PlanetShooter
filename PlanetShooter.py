import pygame
import sys
import random
import os
from time import sleep

#화면 해상도
padWidth = 480   
padHeight = 720

# 폴더안의 이미지를 불러올 수 있도록 하는 코드
current_path = os.path.dirname(__file__)  
image_path = os.path.join(current_path, "PlanetShooter_image") 
sound_path = os.path.join(current_path, "PlanetShooter_sound") 

planetImage = ['PlanetShooter_meteor.png','PlanetShooter_moon.png','PlanetShooter_sun.png','PlanetShooter_sun2.png',\
    'PlanetShooter_planet1.png','PlanetShooter_neptune.png','PlanetShooter_jupiter.png']
# 행성을 맞춘 개수
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 행성 수:' + str(count), True, (0, 255, 255))
    gamePad.blit(text, (10,0))
# 놓친 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 행성:' + str(count), True, (255, 100, 100))
    gamePad.blit(text, (350,0))
# 게임 메시지 출력
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    # 배경음 정지
    pygame.mixer.music.stop()
    gameOverSound.play()
    # 2초간 정지
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()
# 게임 메시지 출력
def writeMessages(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font(None, 120)
    text = textfont.render(text, True, (0, 255, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    winSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()
# 행성충돌시 메시지 출력
def crash():
    global gamePad
    writeMessage('Destroyed!!')
# 게임오버 메시지 출력
def gameOver():
    global gamePad
    writeMessage('Game Over')
# 클리어시 메시지 출력
def gameClear():
    global gamePad
    writeMessages("WIN")

# 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))

def initGame():
    global gamePad, clock, background, plane, missile, explosion, ShotSound, gameOverSound, backgroundSound, winSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    # 게임 이름
    pygame.display.set_caption('PlanetShooter')
    # 배경 이미지
    background = pygame.image.load(os.path.join(image_path, "background.png"))
    # 전투기 이미지
    plane = pygame.image.load(os.path.join(image_path, "plane.png"))
    # 미사일 이미지
    missile = pygame.image.load(os.path.join(image_path, "missile.png"))
    # 폭발 이미지
    explosion = pygame.image.load(os.path.join(image_path, "explosion.png"))
    # 배경 사운드
    backgroundSound = pygame.mixer.music.load(os.path.join(sound_path, "backgroundSound.mp3"))
    pygame.mixer.music.play(-1)
    # 승리 사운드
    winSound = pygame.mixer.Sound(os.path.join(sound_path, "win.mp3"))
    # 발사 사운드
    ShotSound = pygame.mixer.Sound(os.path.join(sound_path, "Shot.mp3"))
    # 패배 사운드
    gameOverSound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.mp3"))

    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, plane, missile, explosion, ShotSound

    # 전투기 크기
    planeSize = plane.get_rect().size
    planeWidth = planeSize[0]
    planeHeight = planeSize[1]
    # 전투기 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.85
    planeX = 0

    # 무기 좌표 리스트
    missileXY = []
    
    # 행성 랜덤 생성
    planet = pygame.image.load(random.choice(planetImage))
    # 행성 크기
    planetSize = planet.get_rect().size
    planetWidth = planetSize[0]
    planetHeight = planetSize[1]
    destroySound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.mp3"))
    # 행성 초기 설정
    planetX = random.randrange(0, padWidth - planetWidth)
    planetY = 0
    planetSpeed = 2

    # 미사일과 운석이 맞으면 True
    isShot = False
    shotCount = 0
    planetPassed = 0

    # Font 정의
    game_font = pygame.font.Font(None, 40)
    total_time = 100
    start_ticks = pygame.time.get_ticks() # 시작 시간 정의

    #게임진행시
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            # 게임 프로그램 종료
            if event.type in [pygame.QUIT]:  
                pygame.quit()
                sys.exit()
            # 키를 누를 경우
            if event.type in [pygame.KEYDOWN]:
                # 전투기 왼쪽 이동
                if event.key == pygame.K_LEFT:
                    planeX -= 5
                # 전투기 오른쪽 이동
                elif event.key == pygame.K_RIGHT:
                    planeX += 5
                # 미사일 발사
                elif event.key == pygame.K_SPACE:
                    ShotSound.play()
                    missileX = x + planeWidth / 2
                    missileY = y - planeHeight
                    missileXY.append([missileX, missileY])
            # 키를 뗄 경우
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    planeX = 0

        # 배경 화면 그리기
        drawObject(background, 0, 0)

        # 전투기 위치 재조정
        x += planeX
        if x < 0:
            x = 0
        elif x > padWidth - planeWidth:
            x = padWidth - planeWidth
        # 전투기와 행성 충돌 체크
        if y < planetY + planetHeight:
            if(planetX > x and planetX < x + planeWidth) or\
                 (planetX + planetWidth > x and planetX + planetWidth < x + planeWidth):
                crash()
        # 전투기 그리기
        drawObject(plane, x, y)

        # 미사일 발사 그리기
        if len(missileXY) != 0:
            # 미사일 요소에 대해 반복할 함수
            for i, bxy in enumerate(missileXY):
                # 미사일 y좌표 -10 ( 위로 이동 시켜줌 )
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                # 미사일이 행성을 맞추면
                if bxy[1] < planetY:
                    if bxy[0] > planetX and bxy[0] < planetX + planetWidth:
                        # 미사일 제거
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                # 미사일이 화면 밖으로 나가면
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
        # 샷카운트
        writeScore(shotCount)
  
        # 행성이 아래로 움직임 (Y 값에서 속도만큼 더해짐)
        planetY += planetSpeed
        # 아래로 떨어질때
        if planetY > padHeight:
            # 새로운 랜덤 행성
            planet = pygame.image.load(random.choice(planetImage))
            planetSize = planet.get_rect().size
            planetWidth = planetSize[0]
            planetHeight = planetSize[1]
            planetX = random.randrange(0, padWidth - planetWidth)
            planetY = 0
            # 놓친 행성 카운트
            planetPassed += 1

        # 5개를 놓치면 패배
        if planetPassed == 5:
            gameOver()
        # 놓친 행성 수 표시
        writePassed(planetPassed)

        # 행성을 맞춘 경우
        if isShot:
            # 행성 폭발시키기
            drawObject(explosion, planetX - 30, planetY) # 폭발그림
            # 폭발 사운드
            destroySound.play()
            # 새로운 랜덤 행성 생성
            planet = pygame.image.load(random.choice(planetImage))
            planetSize = planet.get_rect().size
            planetWidth = planetSize[0]
            planetHeight = planetSize[1]
            planetX = random.randrange(0, padWidth - planetWidth)
            planetY = 0
            # 폭발 사운드
            destroySound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.mp3"))
            isShot = False
            
            # 행성을 맞추면 행성 속도가 증가함
            planetSpeed += 0.15
            # 최대 증가 속도
            if planetSpeed >= 7:
                planetSpeed = 7
        # 행성 그리기
        drawObject(planet, planetX, planetY) 

            # 경과 시간 계산
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 400 # ms -> s
        timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
        drawObject(timer, 180, 0)
    
            # 시간 초과했다면
        if total_time - elapsed_time <= 0:
            gameClear()
        # 게임화면을 다시 그려줌
        pygame.display.update()
        # 게임 화면의 초당 프레임수 설정
        clock.tick(60)
    # pygame 종료
    pygame.quit()

initGame()
runGame()