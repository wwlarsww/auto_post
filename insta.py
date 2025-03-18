import os
import random
import time
import schedule
from instagrapi import Client


class InstagramAccount:
    def __init__(self, username, password, content_folder, delete_after_post=False, post_enabled=True, reel_enabled=True, random_order=True):
        self.username = username
        self.password = password
        self.content_folder = content_folder
        self.delete_after_post = delete_after_post
        self.post_enabled = post_enabled
        self.reel_enabled = reel_enabled
        self.random_order = random_order
        self.client = Client()
        self.logged_in = False
        
    def login(self):
        if not self.logged_in:
            self.client.login(self.username, self.password)
            self.logged_in = True
            print(f"Account logged in:  {self.username}")
            
            
    def get_next_post(self):
        files = [f for f in os.listdir(self.content_folder) if f.endswith((".jpg", ".png", ".mp4"))]
        if not files:
            print("Keine Inhalte zum Posten gefunden.")
            return None, None
        
        files.sort()  # Alphabetische Sortierung
        if self.random_order:
            file = random.choice(files)
        else:
            file = files[0]  # Erstes Element der sortierten Liste nehmen
        
        caption_file = os.path.splitext(file)[0] + ".txt"
        caption_path = os.path.join(self.content_folder, caption_file)
        
        caption = ""
        if os.path.exists(caption_path):
            with open(caption_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()
        
        return os.path.join(self.content_folder, file), caption

    def post(self):
        self.login()  # Login 
        media_path, caption = self.get_next_post()
        if media_path:
            print(f"Poste: {media_path} mit Caption: {caption}")
            
            # If the media is a video and reels are enabled post as reel
            if media_path.endswith(".mp4") and self.reel_enabled: 
                self.client.clip_upload(media_path, caption)
                print("Reel successfully uploaded!")
            
            # If posts are enabled post
            elif self.post_enabled: 
                self.client.photo_upload(media_path, caption)
                print("Post sucsessfully uploaded!")
            
            # If delete_after_post is enabled delete the media and caption
            if self.delete_after_post:
                os.remove(media_path)
                caption_file = os.path.splitext(media_path)[0] + ".txt"
                
                if os.path.exists(caption_file):
                    os.remove(caption_file)
                print("Posted media and caption deleted.")
        else:
            print("No media to post found.")
