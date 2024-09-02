import tt_api
import tt_dataManager
from tt_stockClass import myStock
import tt_functions
import numpy as np
import pandas as pd
import pygame
import json
import os
import io

#TODO: convert to GUI, change function below to trigger on update stock request


def main():
    #temp
    #stockDict = tt_dataManager.updateStocks()
    #stockDict = tt_dataManager.loadStocks()
    screen = pygame.display.set_mode((640, 480))
    width = screen.get_width()
    height = screen.get_height()
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(215, height / 2, 140, 32)
    refresh_box = pygame.Rect(width / 10, height / 10, 32, 32)
    
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('purple')
    color = color_inactive
    active = False
    text = ''
    done = False
    

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                    # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if user clicks refresh button
                if refresh_box.collidepoint(event.pos):
                    stockDict = tt_dataManager.updateStocks()
                    

                else:
                    active = False
                color = color_active if active else color_inactive
            #if event.type == pygame.KEYDOWN[pygame.K_0]:
               # stockDict = tt_dataManager.loadStocks()
            """
            if event.type == pygame.KEYDOWN:
                temp = tt_dataManager.updateStocks()
                if type(temp) == str:
                    print(temp)
                else:
                    stockDict = temp
                    tt_dataManager.saveStocks(stockDict)
                    print("load success")
            """    
        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(32, txt_surface.get_width()+10)
        refresh_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (refresh_box.x+5, refresh_box.y+5))
        # Blit the refresh_box rect.
        pygame.draw.rect(screen, color, refresh_box, 2)
        pygame.draw.rect(screen, color, refresh_box)
        #pygame.image.load(os.path("/tickertape/data/refresh_button.png"))
        #pygame.transform.scale("refresh_button.png", (refresh_box.width, refresh_box.height))

        pygame.display.flip()
        clock.tick(30)

    
    """
    stockList = []
    alphaVantage = tt_api.AlphaVantage("HGC6XVCK2JJ98QD1")
    data = alphaVantage.get_listing_status()
    lines = data.split("\r\n")
    lines.remove(lines[0])
    tickerDict = {}
    for line in lines[:-1]:
        fields = line.split(",")
        #print(fields)
        newStock = myStock(fields[0], fields[1], fields[2], fields[3], fields[4], fields[6])
        stockList.append(newStock)
        #print(newStock)
        #print(len(stockList))
        tickerDict.update({fields[0]:newStock} )
        #newStock.print()
    if len(stockList) == 0:
        print("no more api pulls :(")
    else: 
        tt_dataManager.saveStockList(stockList)#calling the packing function from data manager
        return stockList
    """
    
    
    #for i in range(0,5):
        #print(stockList[i].getTicker())    

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()