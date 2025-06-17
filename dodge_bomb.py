import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {           
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),  
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向の画面内外判定結果
    画面内ならTrue, 画面外ならFalse

    """
    yoko,tate = True,True #初期値：画面の中
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko,tate #画面の中ならTrue, 画面外ならFalse


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))#からのsurfaceを作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery =random.randint(0,HEIGHT)
    vx = +5#爆弾の移動速度
    vy = +5
    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gg_img.set_alpha(50) 
    gg_rct = gg_img.get_rect()
    gg_rct.center = (WIDTH / 2, HEIGHT / 2)  # 半透明の黒背景
    kc_img = pg.image.load("fig/8.png")
    kc_rct1 = kc_img.get_rect()
    kc_rct1.center = (350, HEIGHT / 2) # 左のこうかとんの位置
    kc_rct2 = kc_img.get_rect()
    kc_rct2.center = (WIDTH - 350, HEIGHT / 2) # 右のこうかとんの位置
    fonto = pg.font.Font(None, 80)
    text = fonto.render("GAME OVER", True, (255, 255, 255))# ゲームオーバーのテキスト
    text_rect = text.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2)# テキストの位置を画面中央に設定
    clock = pg.time.Clock()
    tmr = 0
    def gameover(screen: pg.Surface) -> None:
        screen.blit(kc_img,kc_rct1)
        screen.blit(kc_img,kc_rct2)
        screen.blit(gg_img, gg_rct)
        screen.blit(text, text_rect)
        pg.display.update()
        time.sleep(5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出たら
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
