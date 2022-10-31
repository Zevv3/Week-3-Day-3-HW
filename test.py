from datetime import timedelta, date
from IPython.display import Image
import requests
from time import sleep

generic_image = 'codeflix (1).png'



# attributes from instances are unique to that instance
# attributes are protected and only to be accessed by class methods

# skip intro
# fast forward
# subtitles
# favorite

# adding cast list attribute to episode

class Video():
    def __init__(self):
        self.title = None
        self.length = timedelta()
        self.link = generic_image
        self.subtitles = False
        self.sublang = 'English'
        self.favs = []
     
    def set_title(self):
        title = input("What are you watching? ") 
        self.title = title
        
    def subson(self):
        self.subtitles = True
        print(f"{self.sublang} subtitles are now on")
              
    def changelang(self):
        sublang = input("What language? ")
        self.sublang = sublang
        print(f"subtitles are now in {self.sublang}")
              
    def favorites(self):
        
        fav_show = input("What show would you like to add to your favorites?")
        self.favs.append(fav_show)
        fav = input("Would you like to review your favorites?")
        if fav == "y":
            sleep(1)
            print(f"Loading your favorites now..")
            print(self.favs)
        else:
            print("Ok fine then....")
        
        
    
        
    def play(self):
        print(f"Now playing: {self.title}")
        display(Image(self.link))
    def pause(self):
        print("Video Paused")
        
    def __repr__(self):
        return f"{self.title} is {self.length.seconds} seconds long. "

#inheritance as a mixin
class Episode(Video):
    def __init__(self, data):  #<-- add data for passing in our ep
        Video.__init__(self)
        self.number = data['number']
        self.season = data['season']
        self.date_aired = data['airdate']
        self.summary = data['summary']
        self.rating = data['rating']['average']
        self.title = data['name']
        self.length = timedelta(minutes = data['runtime'])
        if data['image']:
            self.link = data['image']['medium']
        else:
            self.link = generic_image


# Video is parent, Episode is the Child. And the Series 
# class grabs from the buffet of Episode class(Mixin Inheritance)

class Series():
    def __init__(self):
        self.id = None
        self.network = None
        self.seasons = None
        self.summary = None
        self.title = None
        self.episode_count = None
        self.genres = []
        self.episodes = []
        self.cast = []
    
    def get_info(self, query = ''):
        data = None #<-- in case the show doesn't come back
        while not data:
            if not query:
                query = input("What is the name of the series? ")
                r = requests.get(f'https://api.tvmaze.com/singlesearch/shows?q={query}')
                if r.status_code == 200:
                    data = r.json()
                else:
                    print(f"Series error: status code {r.status_code}")
                    query = ''
                    
            else:
                r = requests.get(f'https://api.tvmaze.com/singlesearch/shows?q={query}')
                if r.status_code == 200:
                    data = r.json()
                else:
                    print(f"Series error: status code {r.status_code}")
                    query = ''
                
        # use data to build out our attributes
        self.id = data['id']
        self.title = data['name']
        self.summary = data['summary']
        self.genres = [genre for genre in data['genres']]
        if data['network']:
            self.network = data['network']['name']
        else:
            self.network = data['webChannel']['name']
            
        # API call for Episodes
        r = requests.get(f'https://api.tvmaze.com/shows/{self.id}/episodes')
        if r.status_code == 200:
            episodes = r.json()
        else:
            print(f"Episode error: status code {r.status_code}")
            return
        self.seasons = episodes[-1]['season']
        self.episodes = [Episode(ep) for ep in episodes]
        self.episode_count = len(self.episodes)
        
        # API call for the cast
        r = requests.get(f"https://api.tvmaze.com/shows/{self.id}/cast")
        if r.status_code == 200:
            cast = r.json()
        else: 
            print(f"Cast error: status code {r.status_code}")
            return
        self.cast = [person['name'] for person in cast]
    
    def display_info(self):
        print(f"Title: {self.title}\nGenre: {self.genres}\nNumber of Seasons: {self.seasons}\nNumber of Episodes: {self.episode_count}\nSummary: {self.summary}\nCast: {self.cast}")
        break
    def play_show(self):
        for i in range(len(self.episodes)):
            if i > 0 and i % 3 == 0:
                watching = input("Are you still watching? also get a job y/n")
                if watching.lower().strip() not in ('yes', 'y'):
                    break
            self.episodes[i].play() #this comes from our Video class
            sleep(self.episodes[i].length.seconds/1000)
            
    def __len__(self):
        return len(self.episodes)
    
    def __repr__(self):
        return f"Title: {self.title}"
class Theater:
    def __init__(self):
        self.users = []
        self.watch_list = []
        self.current_user = None
        
    # add a user
    def add_user(self, name = ''):
        if not name:
            name = input("What is the name of the new user? ")
        self.users.append(name.title())
        self.choose_user()
        
    # choose a user
    def choose_user(self):
        while True:
            print("Users: ")
            for user in self.users:
                print(user)
            current = input("Choose a user: ")
            if current.title() in self.users:
                self.current_user = current
                break
            else:
                print(f"{current} is not a valid user.")
    
    #add to watchlist
    def add_to_watchlist(self, query = ''):
        show = Series()
        show.get_info(query)
        self.watch_list.append(show)
        print(f"{show.title} has been added to the watchlist! ")
        
    #choose from our watchlist
    def choose_from_watch_list(self):
        for series in self.watch_list:
            print(f"\n\n{series} | Episodes: {len(series)}")
            print(f"\nSummary: \n{series.summary}")
            display(Image(series.episodes[0].link))
        choice = input("Choose a show: ")
        if choice.lower() in list(map(lambda x: x.title.lower(), self.watch_list)):
            action = input("Watch or view details? ")
            if action.lower().strip() in ('watch', 'watch show'):
                for series in self.watch_list:
                    if series.title.lower() == watch.lower().strip():
                        series.play_show()
            if action.lower().strip() in ('view', 'view details', 'details'):
                for series in self.watch_list:
                    if series.title.lower() == watch.lower().strip():
                        series.display_info()
              
                      
                        
        watch = input("What would you like to watch? ")
        if watch.lower() in list(map(lambda x: x.title.lower(), self.watch_list)):
            for series in self.watch_list:
                if series.title.lower() == watch.lower().strip():
                    
        else:
            response = input(f"{watch} is not in your watch list... would you like to add it y/n?")
            
            if response in ('yes','y'):
                self.add_to_watchlist(watch)
                print(".......")
                sleep(2)
                print(".......")
                self.watch_list[-1].play_show()
    
    #run function to drive the program
    def run(self):
        """
        Method allowing users to choose a series and play episodes
        """
        display(Image(generic_image))
        
        if self.users:
            self.choose_user()
        else:
            name = input("Create a profile: ")
            self.add_user(name)
            self.current_user = name
        print("""
            What would you like to do?
            
            Search - Search for shows
            Watch - Pick something from your watch list
            Add User - Add a new user
            Quit - close the application
        """)
        
        while True:
            response = input("What would you like to do? (search, watch, add, quit) ")
            
            if response.lower() == "search":
                self.add_to_watchlist()
            elif response.lower() == "watch":
                self.choose_from_watch_list()
            elif response.lower() in ("add", "add user"):
                self.add_user()
            elif response.lower() == 'quit':
                print(f"Thanks for watching, {self.current_user}! Now go outside!")
                break
            else:
                print("Invalid input, please choose from the list.")