# -*- coding: utf-8 -*-
"""
Created on Wed May 19 21:07:51 2021

@author: simon
"""

import discord
import requests

url = "https://vitemadose.gitlab.io/vitemadose/stats_chronodoses.json"
client = discord.Client()


@client.event
async def on_ready():
    print("Le bot est prêt.")

@client.event
async def on_message(message):
    ctn = message.content
    label = ctn.split()[0]
    if label == ":vac":
        r = requests.get(url)
        rj = r.json()
        lis_dep = rj['departments']
        dep = ctn.split()[1]
        nbVac = lis_dep[dep]
        snd_Mess = "Dans le département " + dep + " il y a " + str(nbVac) + " crénaux de vaccination ouvert à tous faites :centre numeroDeRegion pour avoir les liens de réservation" 
        await message.channel.send(snd_Mess)

    elif label == ":centre":
        url_centre = "https://vitemadose.gitlab.io/vitemadose/" + ctn.split()[1] + ".json"
        req_centre = requests.get(url_centre)
        json_centre = req_centre.json()
        liste_centre = json_centre['centres_disponibles']
        print(liste_centre[0]['appointment_schedules'])
        test = True
        for centre in liste_centre:
            crenaux = centre['appointment_schedules']
            for cren in crenaux:
                if cren['name']=='chronodose':
                    if cren['total'] != 0 :
                        test = False
                        await message.channel.send(centre['url'])
            await message.channel.send("Aucun centre de vaccination ne possède des créneaux ouverts à tous disponibles dans le département choisi")
    elif label == ":help":
        await message.channel.send("tapper \": vac numéro_du_departement\" pour obtenir le nombre de doses disponibles dans le département.")
        await message.channel.send("tapper \": centre numéro_du_departement\" pour obtenir les URL des centres réservables.")

def get_token():
    try:
        file = open("token.txt", "r")
        token = file.read()
        file.close()
        return token
    except:

        print("une erreur est survenue le fichier token.txt n'as pas pus être ouvert")
        return ""
    
client.run(get_token())
