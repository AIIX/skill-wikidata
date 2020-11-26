import re
import sys
import json
import time
from datetime import datetime
import arrow
import requests
from os.path import dirname, join
from bs4 import BeautifulSoup
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.messagebus.message import Message

zurl = "https://www.wikidata.org/entity/"
entity_json = ""

class WikidataSkill(MycroftSkill):
    """
    Wikidata Skill
    """
    def __init__(self):
        super(WikidataSkill, self).__init__(name="WikidataSkill")
    
    def initialize(self):
        self.add_event('skill-wikidata.aiix.home', self.showHome)

    @intent_file_handler('show.wikidata.home.intent')
    def showHome(self, message):
        self.gui.clear()
        self.enclosure.display_manager.remove_active()
        self.displayHome()

    def displayHome(self):
        self.gui.show_page("homepage.qml", override_idle=True)

    @intent_file_handler('birth.place.of.person.intent')
    def handle_wikidata_birthplace_intent(self, message):
        """
        Wikidata BirthPlace Intent
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_birth_place_id = entity_json['entities'][entity_id]['claims']['P19'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_birth_place_response = requests.get(zurl+get_entity_birth_place_id)
                entity_birth_place_json =  get_entity_birth_place_response.json()
                entity_birth_place = entity_birth_place_json['entities'][get_entity_birth_place_id]['labels']['en']['value']
                result_speak = self.translate('birthplace', {'person': person_name, 'place': entity_birth_place})
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = result_speak
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(result_speak)
            except Exception as e:
                notFoundMessage = self.translate('birthplace.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_birth_place = False
        except:
            notFoundMessage = self.translate('birthplace.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_birth_place_id = False

    @intent_file_handler('death.place.of.person.intent')
    def handle_wikidata_deathplace_intent(self, message):
        """
        Wikidata DeathPlace Intent
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_death_place_id = entity_json['entities'][entity_id]['claims']['P20'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_death_place_response = requests.get(zurl+get_entity_death_place_id)
                entity_death_place_json = get_entity_death_place_response.json()
                entity_death_place = entity_death_place_json['entities'][get_entity_death_place_id]['labels']['en']['value']
                result_speak = self.translate('deathplace',
                                              {'person': person_name,
                                               'place': entity_death_place})
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = result_speak
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(result_speak)
            except Exception as e:
                notFoundMessage = self.translate('deathplace.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_death_place = False
        except:
            notFoundMessage = self.translate('deathplace.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_death_place_id = False

    @intent_file_handler('how.old.is.person.intent')
    def handle_wikidata_age_intent(self, message):
        """
        Wikidata SearchAge Intent
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_dob_id = entity_json['entities'][entity_id]['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
            try:
                fix_gedid = get_entity_dob_id.replace("+", "") 
                a = arrow.get(fix_gedid)
                birth_date = a.format("DD/MM/YYYY")
                dob = birth_date
                dob = datetime.strptime(dob, '%d/%m/%Y')
                age = ("%d" % ((datetime.today() - dob).days/365))
                result_msg = self.translate('age', {'person': person_name,
                                                    'age': age})
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = result_msg
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(result_msg)
            except Exception as e:
                notFoundMessage = self.translate('age.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_death_place = False
        except:
            notFoundMessage = self.translate('age.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_death_place_id = False

    @intent_file_handler('what.is.the.gender.intent')
    def handle_wikidata_gender_intent(self, message):
        """
        Wikidata Gender Intent
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_gender_id = entity_json['entities'][entity_id]['claims']['P21'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_gender_id_response = requests.get(zurl+get_entity_gender_id)
                entity_gender_id_json =  get_entity_gender_id_response.json()
                entity_gender = entity_gender_id_json['entities'][get_entity_gender_id]['labels']['en']['value']
                self.speak(entity_gender)
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_gender
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_gender)
            except Exception as e:
                notFoundMessage = self.translate('gender.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_gender_id = False
        except:
            notFoundMessage = self.translate('gender.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_gender_id = False

    @intent_file_handler('who.is.the.spouse.intent')
    def handle_wikidata_spouse_intent(self, message):
        """
        Wikidata Spouse Intent
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_spouse_id = entity_json['entities'][entity_id]['claims']['P26'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_spouse_id_response = requests.get(zurl+get_entity_spouse_id)
                entity_spouse_id_json = get_entity_spouse_id_response.json()
                entity_spouse_id = entity_spouse_id_json['entities'][get_entity_spouse_id]['labels']['en']['value']
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_spouse_id
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_spouse_id)
            except Exception as e:
                notFoundMessage = self.translate('spouse.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_spouse_id = False
        except:
            notFoundMessage = self.translate('spouse.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_spouse_id = False

    @intent_file_handler('which.country.is.from.intent')
    def handle_wikidata_country_citizenship(self, message):
        """
        Wikidata Country Citizenship
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_country_citizenship_id = entity_json['entities'][entity_id]['claims']['P27'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_country_citizenship_id_response = requests.get(zurl+get_entity_country_citizenship_id)
                entity_country_citizenship_json = get_entity_country_citizenship_id_response.json()
                entity_country_citizenship = entity_country_citizenship_json['entities'][get_entity_country_citizenship_id]['labels']['en']['value']
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_country_citizenship
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_country_citizenship)
            except Exception as e:
                notFoundMessage = self.translate('country.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_country_citizenship = False
        except:
            notFoundMessage = self.translate('country.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_country_citizenship_id = False

    @intent_file_handler('what.children.name.intent')
    def handle_wikidata_child_name(self, message):
        """
        Wikidata Child Name
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_child_id = entity_json['entities'][entity_id]['claims']['P40'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_child_id_response = requests.get(zurl+get_entity_child_id)
                entity_child_id_json = get_entity_child_id_response.json()
                entity_child_id = entity_child_id_json = entity_child_id_json['entities'][get_entity_child_id]['labels']['en']['value']
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_child_id
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_child_id)
            except Exception as e:
                notFoundMessage = self.translate('children.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_child_id = False
        except:
            notFoundMessage = self.translate('children.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_child_id = False

    @intent_file_handler('what.occupation.intent')
    def handle_wikidata_occupation(self, message):
        """
        Wikidata Occupation
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_occupation_id = entity_json['entities'][entity_id]['claims']['P106'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_occupation_id_response = requests.get(zurl+get_entity_occupation_id)
                entity_occupation_id_json = get_entity_occupation_id_response.json()
                entity_occupation_id = entity_occupation_id_json['entities'][get_entity_occupation_id]['labels']['en']['value']
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_occupation_id
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_occupation_id)
            except Exception as e:
                notFoundMessage = self.translate('occupation.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_occupation_id = False
        except:
            notFoundMessage = self.translate('occupation.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_occupation_id = False

    @intent_file_handler('burial.location.intent')
    def handle_wikidata_place_of_burial(self, message):
        """
        Wikidata Place Of Burial
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']

        try:
            get_entity_place_of_burial_id = entity_json['entities'][entity_id]['claims']['P119'][0]['mainsnak']['datavalue']['value']['id']
            try:
                get_entity_place_of_burial_id_response = requests.get(zurl+get_entity_place_of_burial_id)
                entity_place_of_burial_id_json = get_entity_place_of_burial_id_response.json()
                entity_place_of_burial_id = entity_place_of_burial_id_json['entities'][get_entity_place_of_burial_id]['labels']['en']['value']
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = entity_place_of_burial_id
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(entity_place_of_burial_id)
            except Exception as e:
                notFoundMessage = self.translate('burial.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_place_of_burial_id = False
        except:
            notFoundMessage = self.translate('burial.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_place_of_burial_id = False

    @intent_file_handler('date.of.birth.intent')
    def handle_wikidata_date_of_birth(self, message):
        """
        Wikidata Date of Birth
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_dob_id = entity_json['entities'][entity_id]['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
            try:
                fix_gedobid = get_entity_dob_id.replace("+", "")
                a = arrow.get(fix_gedobid)
                birth_date = a.format("DD,MM,YYYY")
                birth_date_breakup = birth_date.split(",")
                person_name = message.data['person']
                day = birth_date_breakup[0]
                month = birth_date_breakup[1]
                year = birth_date_breakup[2]
                birth_date_to_speak = self.translate('date.of.birth',
                                                     {'person': person_name,
                                                      'day': day,
                                                      'month': month,
                                                      'year': year})
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = birth_date
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(birth_date_to_speak)
            except Exception as e:
                notFoundMessage = self.translate('date.of.birth.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_dob = False
        except:
            notFoundMessage = self.translate('date.of.birth.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_dob_id = False

    @intent_file_handler('date.of.death.intent')
    def handle_wikidata_date_of_death(self, message):
        """
        Wikidata Date of Death
        """
        global entity_json
        entity_id = self.getEntityId(message.data['person'])
        person_name = message.data['person']
        thumb_image = self.always_get_image(entity_id)
        try:
            get_entity_dod_id = entity_json['entities'][entity_id]['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
            try:
                fix_gedodid = get_entity_dod_id.replace("+", "")
                a = arrow.get(fix_gedodid)
                death_date = a.format("DD,MM,YYYY")
                death_date_breakup = death_date.split(",")
                person_name = message.data['person']
                day = death_date_breakup[0]
                month = death_date_breakup[1]
                year = death_date_breakup[2]
                death_date_to_speak = self.translate('date.of.death',
                                                     {'person': person_name,
                                                      'day': day,
                                                      'month': month,
                                                      'year': year})
                self.gui.clear()
                self.gui["personContext"] = person_name
                self.gui["answerData"] = death_date
                self.gui["imgLink"] = thumb_image
                self.gui.show_page("answer.qml", override_idle=30)
                self.speak(death_date_to_speak)
            except Exception as e:
                notFoundMessage = self.translate('date.of.death.not.found',
                                                 {'person': person_name})
                self.speak(notFoundMessage)
                entity_dod = False
        except:
            notFoundMessage = self.translate('date.of.death.not.found',
                                             {'person': person_name})
            self.speak(notFoundMessage)
            get_entity_dob_id = False

    def getAge(self, dateofbirth):
        d = datetime.strptime(s, '%d %B, %Y')
        print(d.strftime('%Y-%m-%d'))
        return d.strftime('%Y-%m-%d')

    def get_info_wikidata(self, datavalue):
        name = datavalue.strip()
        wikidataObject = self._wikidata(name)
        r = wikidataObject['search'][0]['concepturi']
        return r

    def _wikidata(self, name):
        url = "http://www.wikidata.org/w/api.php"
        params = {
            "search": name,
            "action": "wbsearchentities",
            "format": "json",
            "language": "en",
            "type": "item",
            "continue": "0",
            "limit": "10"
        }
        return requests.get(url, params=params).json()


    def getEntityId(self, itemcontext):
        item = itemcontext
        global entity_json
        try:
            result = self.get_info_wikidata(item)
            if result != None:
                entity_result = requests.get(result)
                entity_json = entity_result.json()
                for key in entity_json['entities'].keys():
                    entity_id = key
                    return entity_id
        except:
            return False

    def always_get_image(self, datakey):
            global entity_json
            entity_id = datakey
            try:
                get_entity_pic_link = entity_json['entities'][entity_id]['claims']['P18'][0]['mainsnak']['datavalue']['value']
                get_entity_pic = get_entity_pic_link.replace(" ", "_")
                get_entity_pic_hyperlink = "https://commons.wikimedia.org/wiki/File:{0}".format(get_entity_pic)
                get_entity_pic_content = requests.get(get_entity_pic_hyperlink)
                soup = BeautifulSoup(get_entity_pic_content.content, 'html.parser')
                imagelist = []
                for link in soup.find_all('div', class_="fullImageLink"):
                    for x in link.find_all('a'):
                        r = x.get('href')
                        imagelist.append(r)

                return imagelist[0]
            except:
                get_entity_pic_link = False
                print(get_entity_pic_link)
                return False

    def stop(self):
        pass


def create_skill():
    return WikidataSkill()
