# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    '''
    A NewsStory has five attributes:
    self.guid  (string, globally unique identifier)
    self.title (string)
    self.description (string)
    self.link (string)
    self.pubdate (string, a datetime)
    '''
    def __init__(self,guid,title,description,link,pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link 
        self.pubdate = pubdate
    
    def get_guid(self):
        '''
        Used to safely access self.guid outside the class

        Returns: self.guid
        '''
        return self.guid
    
    def get_title(self):
        '''
        Used to safely access self.title outside the class

        Returns: self.title
        '''
        return self.title
    
    def get_description(self):
        '''
        Used to safely access self.descroiption outside the class

        Returns: self.description
        '''
        return self.description
    
    def get_link(self):
        '''
        Used to safely access self.link outside the class

        Returns: self.link
        '''
        return self.link
    
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside the class

        Returns: self.pubdate
        '''
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
        
        # story (NewsStory): a news story
        # output (Binary)
        


# PHRASE TRIGGERS



# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    '''
    Constructor used to initialize a phrase string
    
    self.phrase: string, a phrase which if found in the text generates an alert. It is assumed to not contain any punctuation.
    '''
    def __init__(self,phrase):
        self.phrase = phrase
        
        
    def is_phrase_in(self,text):
        '''
        Takes a string text and returns true if the whole phrase is present in text
        
        text: string, the text which might contain the phrase
            
        Returns: Binary out put if text contains the phrase
        -------
        '''
        #self.text = text.lower
        # Manipulate text to be suitable for comparison to phrase
        
        # Replace punctuation by a space and make everything lowercase for the text and phrase
        no_punct_list = [char  if char not in string.punctuation else ' ' for char in text.lower()]
        no_punct_text = ''.join(no_punct_list)
        clean_list =  no_punct_text.split()
        clean_text = ' '.join(clean_list)+' '
        
        
        no_punct_list = [char  if char not in string.punctuation else ' ' for char in self.phrase.lower()]
        no_punct_text = ''.join(no_punct_list)
        clean_list =  no_punct_text.split()
        clean_phrase = ' '.join(clean_list)+' '
        
        # Search the text for the phrase        
        if clean_phrase in clean_text:
            return True
        else:
            return False


        


#Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
    

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def __init__(self,time_str):
        ''' Initiates the TimeTrigger class.
            Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
            Convert time from string to a datetime before saving it as an attribute.
        '''
        # Convert time from string to a datetime
        time = datetime.strptime(time_str,'%d %b %Y %H:%M:%S')
        
        # Save the time as an attribute
        self.time = time

    
    
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self,story):
        ''' Returns True if the publication date is strictly before the trigger time.'''
        # Try to compare the trigger and publication times
        try: 
            cond = story.get_pubdate()<self.time
        # Otherwise fixt the timezone
        except:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            cond =  story.get_pubdate()<self.time
        
        if cond:      
            return True 
        else:
            return False

class AfterTrigger(TimeTrigger):
    def evaluate(self,story):
        ''' Returns True if the publication date is strictly after the trigger time.'''
        # Try to compare the trigger and publication times
        try: 
            cond = story.get_pubdate()>self.time
        # Otherwise fixt the timezone
        except:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            cond =  story.get_pubdate()>self.time
        
        if cond:      
            return True 
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    ''' Performs a logical NOT operation on a trigger.'''
    def __init__(self,Trig):
        self.Trig = Trig
    
    def evaluate(self,story):
        return not self.Trig.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    ''' Performs a logical AND operation on two triggers Trig1 and Trig2.'''
    def __init__(self,Trig1,Trig2):
        self.Trig1 = Trig1
        self.Trig2 = Trig2
        
    def evaluate(self, story):
        return self.Trig1.evaluate(story) and self.Trig2.evaluate(story)
    
# Problem 9
class OrTrigger(Trigger):
    ''' Performs a logical OR on Trig1 and Trig2.'''
    def __init__(self,Trig1,Trig2):
        self.Trig1 = Trig1
        self.Trig2 = Trig2
        
    def evaluate(self, story):
        return self.Trig1.evaluate(story) or self.Trig2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # The list which will contain the strories which include the triggers.
    filt_list = []
    # Run over all the stories and triggers and check if any of the triggers fire. 
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filt_list.append(story)
                break
    return filt_list



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
            
    # line is the list of lines that you need to parse and for which you need
    # to build triggers            
    
    # Map
    T_map = {'TITLE': TitleTrigger,'DESCRIPTION': DescriptionTrigger,
             'TIME':TimeTrigger,'BEFORE':BeforeTrigger,'AFTER':AfterTrigger,
             'NOT':NotTrigger,'AND':AndTrigger,'OR':OrTrigger}
             
    trig_dict = {}
    triggers = []
    
    for l in lines:
        # split the lines into words
        l_list = l.split(',')
        # Defining new triggers
        if l_list[0] != 'ADD':
            trigger_type = l_list[1]
            if trigger_type == 'AND' or trigger_type == 'OR':               
                trig_dict[l_list[0]] = T_map[trigger_type](l_list[2],l_list[3])
            else:    
                trig_dict[list[0]] = T_map[trigger_type](l_list[2])
        else:
            triggers = [trig_dict[t] for t in l_list[1:] ]
    return triggers


    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

