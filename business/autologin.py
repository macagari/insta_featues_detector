from playwright.sync_api import sync_playwright
import shutil
import os
import time
import re

from utils.logger_utils import stream_logger

logger = stream_logger(__name__)

def extract_images() :
    username = ""
    password = ""
    images_number = ""
    timeout = ""
    profiles = []

    with open("config.txt", "r") as config_file:
        for line in config_file.readlines():
            key_value = line.strip().split(":")
            username = key_value[1] if (key_value[0] == "username") else username
            password = key_value[1] if (key_value[0] == "password") else password
            images_number = int(key_value[1]) if (key_value[0] == "images_number") else images_number
            timeout = int(key_value[1]) if (key_value[0] == "timeout") else timeout
            profiles.append(key_value[1]) if (key_value[0] == "profiles") else profiles
            profiles.append(key_value[0]) if (":" not in line) else profiles

    current_profile_index = 0
    MAX_PICTURE_INSTAGRAM = images_number
    website_list = ["instagram"]#	,"gelocal","ilcentro","ilgiorno","ilmattino","ilrestodelcarlino","lanazione","lanuovasardegna","lastampa"]
    website_list_filename = website_list[0]
    print("START")

    endpoint_names = []
    for current_login_file in website_list:
        with open(current_login_file+".txt", 'r', encoding='utf-8') as instructions:
            for line in instructions:
                if (line == "\n" or line[0] == "#"):
                    #print("[ SKIPPED LINE ] ", line)
                    continue
                tokens = line.split("------")
                INSTRUCTION = tokens[0].strip()
                ## GOTO
                if (INSTRUCTION.upper() == "GOTO"):
                    click_number = 1
                    endpoint_name = tokens[1]
                    endpoint_names.append(endpoint_name)

        for current_endpoint_name in endpoint_names:
            try:
                shutil.rmtree(current_endpoint_name)
                print("DIRECTORY RIMOSSA",current_endpoint_name)
            except:
                print("DIRECTORY INESISTENTE",current_endpoint_name)
        last_taken_selector = ""
        last_number_of_occurrences = 0
        last_number_of_occurrences_column = 0
        last_number_of_occurrences_row = 0
        endpoint_name=""
        instagram_step=0
        prefix=65
        with sync_playwright() as p:
            print("iniziato")
            browser = p.webkit.launch()
            page = browser.new_page()
            with open(website_list_filename+".txt", 'r', encoding='utf-8') as instructions:
                click_number = 1
                for line in instructions:
                    if(prefix>122):
                        prefix=65
                    if(90<prefix<97):
                        prefix = 97
                    if(len(line)==0 or line=="\n" or line[0]=="#"):
                        print("[ SKIPPED LINE ] ",line)
                        continue
                    tokens = line.split("------")
                    INSTRUCTION = tokens[0].strip().upper()

                    ## GOTO
                    if(INSTRUCTION.upper()=="GOTO"):
                        click_number = 1
                        endpoint = tokens[2].strip()
                        try:
                            os.mkdir(tokens[1])
                            endpoint_name = tokens[1]
                            print("[GOTO] ", endpoint_name, " all'indirizzo:", endpoint)
                        except:
                            print("[GOTO] STIAMO APRENDO UN NUOVO LINK:",endpoint," MA RESTEREMO SOTTO LA STESSA DIR DEL PRIMO LINK APERTO")
                        try:
                            page.goto(endpoint)
                            page.screenshot(path=endpoint_name + "/" + chr(prefix)+"_GOTO.png")
                            prefix+=1
                            print("[GOTO] Done.")
                        except Exception as ex:
                            print("[GOTO] Errore durante GOTO ",endpoint_name," all'indirizzo:",endpoint,"--->",str(ex))
                        if("Instagram/" in endpoint_name):
                            line = "COUNT_REGEX_OCCURRENCES_INSTAGRAM------Nnq7C weEfm------v1Nh3 kIKUG _bz0w"
                            tokens = line.split("------")
                            INSTRUCTION = tokens[0].strip().upper()
                            instagram_step=1
                    ## GOTO
                    if(INSTRUCTION.upper()=="GOTO_DEEP_INSTAGRAM"):
                        logger.debug("profiles:"+str(profiles)+" current_profile_index:"+str(current_profile_index))
                        if(len(profiles)==current_profile_index):
                            logger.debug("Instagram extraction completed.")
                            return True
                        page.set_default_navigation_timeout(timeout)
                        page.set_default_timeout(timeout)
                        click_number = 1
                        endpoint = "https://www.instagram.com/"+profiles[current_profile_index].strip()+"/"
                        try:
                            os.mkdir("Instagram/"+profiles[current_profile_index])
                            endpoint_name = "Instagram/"+profiles[current_profile_index]
                            print("[GOTO_DEEP_INSTAGRAM] ", endpoint_name, " all'indirizzo:", endpoint)
                        except:
                            print("[GOTO_DEEP_INSTAGRAM] STIAMO APRENDO UN NUOVO LINK:",endpoint," MA RESTEREMO SOTTO LA STESSA DIR DEL PRIMO LINK APERTO")
                        try:
                            page.goto(endpoint)
                            waiting_seconds = 10
                            print("[GOTO_DEEP_INSTAGRAM] waiting for...",waiting_seconds)
                            time.sleep(waiting_seconds)
                            print("[GOTO_DEEP_INSTAGRAM] ...waited!")
                            page.screenshot(path=endpoint_name + "/" + chr(prefix)+"_GOTO.png")
                            prefix+=1
                            print("[GOTO_DEEP_INSTAGRAM] Done.")
                        except Exception as ex:
                            print("[GOTO_DEEP_INSTAGRAM] Errore durante GOTO ",endpoint_name," all'indirizzo:",endpoint,"--->",str(ex))

                        current_profile_index += 1
                        # CLICKING THE PICTURE UPPER LEFT
                        selector = "//html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]"

                        selector_was_ok = False
                        try:
                            number_of_selectors_found = page.locator(selector).count()
                            if number_of_selectors_found > 1:
                                print("[GOTO_DEEP_INSTAGRAM CLICK] Multiple selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                print("[GOTO_DEEP_INSTAGRAM CLICK] First one:",page.locator(selector).first)
                                print("[GOTO_DEEP_INSTAGRAM CLICK] Last one:",page.locator(selector).last)
                                page.locator(selector).last.click()
                            else:
                                print("[GOTO_DEEP_INSTAGRAM CLICK] <1 selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                page.locator(selector).click()
                            selector_was_ok = True
                        except Exception as ex:
                            print("[GOTO_DEEP_INSTAGRAM CLICK] ",str(ex)," Error using selector ",selector,"\n trying with another one..")
                            selector_was_ok = False

                        if not selector_was_ok:
                            try:
                                selector = "//html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]"
                                number_of_selectors_found = page.locator(selector).count()
                                if number_of_selectors_found > 1:
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] Multiple selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] First one:",page.locator(selector).first)
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] Last one:",page.locator(selector).last)
                                    page.locator(selector).last.click()
                                else:
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] <1 selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                    page.locator(selector).click()
                                selector_was_ok = True
                            except Exception as ex:
                                print("[GOTO_DEEP_INSTAGRAM CLICK] ",str(ex)," Error using selector ",selector,"\n trying with another one..")
                                selector_was_ok = False
                        if not selector_was_ok:
                            print("[GOTO_DEEP_INSTAGRAM CLICK] Error using selector ",selector,"\n give up for this profile...")
                        print("sleeping now..")
                        time.sleep(2)
                        print("taking screenshot..")
                        screenshot_succeeded = False
                        instagram_row = 1
                        instagram_column = 1
                        page.screenshot(path=endpoint_name + "/" + chr(prefix)+"_IMAGE_"+str(instagram_row)+"_"+str(instagram_column)+".png")

                        picture_count = 0
                        while picture_count < MAX_PICTURE_INSTAGRAM:
                            picture_count += 1
                            try:
                                current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div[3]"

                                print("[GOTO_DEEP_INSTAGRAM GET PICTURE] trying CHECKING IF IT IS A VIDEO ... ",current_selector)
                                page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(picture_count)+"_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                screenshot_succeeded = True
                            except Exception as ex:
                                screenshot_succeeded = False
                                current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div/div[1]/div[2]"
                                print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex)+".\n Trying with..",current_selector)

                            if not screenshot_succeeded:
                                try:
                                    page.locator(current_selector).screenshot(
                                        path=endpoint_name + "/" + chr(prefix) + "_" + "instagram_profile_" + str(
                                            picture_count) + "_" + str(instagram_row) + "_" + str(
                                            instagram_column) + ".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[2]"
                                    print(
                                        "[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of" + str(
                                            ex) + ".\n Trying with..", current_selector)

                            if not screenshot_succeeded:
                                try:
                                    page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(picture_count)+"_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[2]"
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex)+".\n Trying with..",current_selector)


                            if not screenshot_succeeded:
                                try:
                                    page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(picture_count)+"_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex))

                            if screenshot_succeeded:
                                print("[GOTO_DEEP_INSTAGRAM GET PICTURE] OK PICTURE TAKEN! --> Now let's take the next one")
                            else:
                                print("[GOTO_DEEP_INSTAGRAM GET PICTURE] CURRENT PICTURE NOT TAKEN! --> Now let's take the next one")
                            #page.locator("//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button/div/span/svg").click()
                            #page.locator("//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button").click()
                            page.keyboard.press('ArrowRight')
                            print("[GOTO_DEEP_INSTAGRAM GET PICTURE] pressed right arrow! Waiting 1 seconds..")
                            time.sleep(1)
                            print("[GOTO_DEEP_INSTAGRAM GET PICTURE] .... waited!")

                        '''
                        for instagram_row in [1,2,3]:
                            for instagram_column in [1,2,3]:
                                selector = "//html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[3]/article/div[1]/div/div[ROW]/div[COLUMN]".replace("ROW",str(instagram_row)).replace("COLUMN",str(instagram_column))
                                number_of_selectors_found = page.locator(selector).count()
                                if number_of_selectors_found > 1:
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] Multiple selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] First one:",page.locator(selector).first)
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] Last one:",page.locator(selector).last)
                                    page.locator(selector).last.click()
                                else:
                                    print("[GOTO_DEEP_INSTAGRAM CLICK] <1 selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                    page.locator(selector).click()
                                print("sleeping now..")
                                time.sleep(2)
                                print("taking screenshot..")
                                screenshot_succeeded = False
                                page.screenshot(path=endpoint_name + "/" + chr(prefix)+"_IMAGE_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                try:
                                    current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div/div[2]"
                                                        
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] trying taking image... ",current_selector)
                                    page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div/div[1]/div[2]"
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex)+".\n Trying with..",current_selector)
                                
                                if screenshot_succeeded:
                                    continue
                                try: 
                                    page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    current_selector = "//html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[2]"
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex)+".\n Trying with..",current_selector)
                                    
                                
                                if screenshot_succeeded:
                                    continue
                                try:
                                    page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(instagram_row)+"_"+str(instagram_column)+".png")
                                    screenshot_succeeded = True
                                except Exception as ex:
                                    screenshot_succeeded = False
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] previous selector didn't work, because of"+str(ex))
                                
                                if screenshot_succeeded:
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] OK PICTURE TAKEN!")
                                else:                            
                                    print("[GOTO_DEEP_INSTAGRAM GET PICTURE] CURRENT PICTURE NOT TAKEN!")
                        '''
                        if("Instagram/" in endpoint_name):
                            line = "CLICK_PICTURE_XPATH------//html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[3]/article/div[1]/div/div[ROW]/div[COLUMN]"
                            tokens = line.split("------")
                            INSTRUCTION = tokens[0].strip().upper()
                            instagram_step=1

                        '''
                        if("Instagram/" in endpoint_name):
                            line = "COUNT_REGEX_OCCURRENCES_INSTAGRAM_DEEP------Nnq7C weEfm------v1Nh3 kIKUG _bz0w"
                            tokens = line.split("------")
                            INSTRUCTION = tokens[0].strip().upper()
                            instagram_step=1
                        '''

                    #WAIT_FOR_A_GIVEN_TIME
                    if(INSTRUCTION.upper()=="WAIT_FOR_SECONDS"):
                        step_secondi = 5
                        seconds = int(tokens[1])
                        try:
                            step_secondi = int(tokens[2])
                        except:
                            None
                        print("[WAIT_FOR_SECONDS] Waiting for",seconds," seconds......",end="")
                        secondi_trascorsi=0
                        while(secondi_trascorsi<seconds):
                            time.sleep(step_secondi)
                            secondi_trascorsi+=step_secondi
                            page.screenshot(path=endpoint_name + "/" +chr(prefix)+ "_SLEEP_"+str(secondi_trascorsi)+".png")
                            prefix+=1
                        print("... Done! :D ")

                    #CLICK_IN_IFRAME
                    if(INSTRUCTION.upper()=="CLICK_IN_IFRAME"):
                        iframe_ID = tokens[1].strip()
                        selector = tokens[2].strip()
                        if(iframe_ID=="LAST_TAKEN_SELECTOR"):
                            iframe_ID = last_taken_selector
                        page.screenshot(path=endpoint_name + "/"+chr(prefix)+"_CLICK_IN_IFRAME" +iframe_ID+selector +".png")
                        prefix+=1
                        print("[CLICK_IN_IFRAME] ", endpoint_name, " iframe ", iframe_ID, " selector ",selector)
                        try:
                            iframe = page.query_selector(iframe_ID).content_frame()
                            print("[CLICK_IN_IFRAME] iframe!  --->",iframe)
                            time.sleep(10)
                            element = iframe.locator(selector)
                            print("[CLICK_IN_IFRAME] element!  --->",element)
                            clicked = element.click()

                            print("[CLICK_IN_IFRAME] clicked!  --->",clicked)
                        except Exception as ex:
                            print("[CLICK_IN_IFRAME] Errore durante CLICK_IN_IFRAME ",endpoint_name," all'indirizzo:",endpoint,"iframe_ID",iframe_ID,"selector",selector,"\n[CLICK_IN_IFRAME EXCEPTION]--->",str(ex))

                    #CLICK_IN_IFRAME
                    if(INSTRUCTION.upper()=="FILL_IN_IFRAME" or INSTRUCTION.upper()=="USERNAME_IN_IFRAME" or INSTRUCTION.upper()=="PASSWORD_IN_IFRAME"):
                        payload_string = tokens[1].strip()
                        iframe_ID = tokens[2].strip()
                        selector = tokens[3].strip()

                        if(iframe_ID=="LAST_TAKEN_SELECTOR"):
                            iframe_ID = last_taken_selector
                        page.screenshot(path=endpoint_name + "/"+chr(prefix)+"_PRIMA_"+INSTRUCTION+"_"+iframe_ID+selector +"_"+payload_string+".png")
                        prefix+=1
                        print("["+INSTRUCTION+"]",payload_string, endpoint_name, " iframe ", iframe_ID, " selector ",selector)
                        try:
                            iframe = page.query_selector(iframe_ID).content_frame()
                            print("["+INSTRUCTION+"]"+" iframe!  --->",iframe)
                            time.sleep(10)
                            element = iframe.locator(selector)
                            print("["+INSTRUCTION+"]"+" element!  --->",element)
                            clicked = element.fill(payload_string)
                            print("["+INSTRUCTION+"]"+" clicked!  --->",clicked)
                            page.screenshot(path=endpoint_name + "/" + chr(prefix) + "_DOPO_" + INSTRUCTION + "_" + iframe_ID + selector + "_" + payload_string + ".png")
                        except Exception as ex:
                            print("["+INSTRUCTION+"]"+" Errore durante FILL_IN_IFRAME ",endpoint_name," all'indirizzo:",endpoint,"iframe_ID",iframe_ID,"selector",selector,"\n["+INSTRUCTION+"]"+str(ex))

                    ## CLICK SELECTOR syntax: CLICK selector
                    if(INSTRUCTION.upper()=="CLICK"):
                        selector = tokens[1].strip()
                        print("[CLICK] " + str(click_number)," -->", endpoint_name, " -->", selector)
                        try:
                            number_of_selectors_found = page.locator(selector).count()
                            if number_of_selectors_found > 1:
                                print("[CLICK] Multiple selectors found: -->",number_of_selectors_found,"<--",page.locator(selector))
                                print("[CLICK] First one:",page.locator(selector).first)
                                print("[CLICK] Last one:",page.locator(selector).last)
                                page.locator(selector).last.click()
                            else:
                                page.locator(selector).click()
                            page.screenshot(path=endpoint_name + "/"+chr(prefix)+"_CLICK_" + str(click_number) + ".png")
                            prefix += 1
                            print("[CLICK] Clicked.")

                        except Exception as ex:
                            print("[CLICK] Errore durante CLICK_" + str(click_number)," -->", endpoint_name, " -->", selector)
                            print("[CLICK] Exception:"+str(ex))
                        click_number += 1

                    ## FILL SELECTOR syntax: FILL text selector
                    if(INSTRUCTION.upper()=="GENERIC_FILL_BOX" or INSTRUCTION.upper()=="FILL" or INSTRUCTION.upper()=="USERNAME" or INSTRUCTION.upper()=="PASSWORD"):
                        #box_input = tokens[1]
                        box_input = username
                        selector = tokens[2].strip()
                        print("[FILL] " +box_input+" in:"+ INSTRUCTION +" -->", endpoint_name, " -->", selector)
                        try:
                            page.locator(selector).fill(box_input)
                            page.screenshot(path=endpoint_name + "/"+chr(prefix)+"_FILL_" + INSTRUCTION + ".png")
                            prefix+=1
                            print("[FILL] Filled.")
                        except Exception as ex:
                            print("[FILL] Errore durante FILL " + str(click_number)," -->", endpoint_name, " -->", selector)
                            print("[FILL] Eccezione:",str(ex))
                    ## FILL SELECTOR syntax: FILL text selector
                    if(INSTRUCTION.upper()=="PASSWORD_CRYPTED"):
                        box_input = tokens[1]
                        selector = tokens[2].strip()
                        print("[PASSWORD_CRYPTED] " +box_input+" in:"+ INSTRUCTION +" -->", endpoint_name, " -->", selector)
                        decrypted_box_input=""
                        for char in box_input:
                            decrypted_box_input+=chr(ord(char)-1)
                        #box_input=decrypted_box_input
                        box_input = password
                        print("PASS:",box_input)
                        try:
                            page.locator(selector).fill(box_input)
                            page.screenshot(path=endpoint_name + "/"+chr(prefix)+"_FILL_" + INSTRUCTION + ".png")
                            prefix+=1
                            print("[PASSWORD_CRYPTED] Filled.")
                        except:
                            print("[PASSWORD_CRYPTED] Errore durante CLICK_" + str(click_number)," -->", endpoint_name, " -->", selector)

                    ## WAIT
                    if(INSTRUCTION.upper()=="WAIT_FOR" or INSTRUCTION.upper()=="WAIT" or INSTRUCTION.upper()=="WAIT_SELECTOR"):
                        wanted_selector = tokens[1].strip()
                        print("[WAIT] "+INSTRUCTION+"_"+wanted_selector)
                        i=0
                        loop = True
                        while loop:
                            result = page.locator(wanted_selector).count()
                            corrected_filepath = endpoint_name + "/" +str(chr(prefix)+"_"+ INSTRUCTION + "_" + wanted_selector[:int(len(wanted_selector) / 5)] + ".png").replace("/","_")
                            page.screenshot(path=corrected_filepath)
                            prefix+=1
                            time.sleep(1)
                            print("number of found selectors:",result)
                            i+=1
                            if(result>0):
                                loop = False
                        print("[WAIT] Done! :D :D :D")

                    ## LOOP
                    if(INSTRUCTION.upper()=="LOOP_SCREENSHOTS"):
                        print("[LOOP_SCREENSHOTS] ENTRO IN LOOP ",endpoint_name)
                        i=0
                        loop = True
                        while loop:
                            i+=1
                            page.screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+ INSTRUCTION + "_" + str(i) + ".png")
                            prefix+=1
                            time.sleep(5)

                    ## READ
                    if (INSTRUCTION.upper() == "READ"):
                        print("[READ] ENTRO IN READ ", endpoint_name)
                        selector = tokens[1].strip()
                        print("[READ] " + str(selector), " -->", endpoint_name)
                        try:
                            value = page.locator(selector).inner_text()
                            print("[READ] HO LETTO QUESTO VALORE---->", value)
                        except Exception as ex:
                            print("[READ] Errore durante READ" + endpoint_name, " -->", selector, "---->", str(ex))

                    ## CHECK_VALUE
                    if (INSTRUCTION.upper() == "CHECK_VALUE"):
                        print("[CHECK_VALUE] ENTRO IN CHECK_VALUE ", endpoint_name)
                        selector = tokens[1].strip()
                        value_to_be_checked = tokens[2].strip()
                        print("[CHECK_VALUE] selector--->" + str(selector), " endpoint-->", endpoint_name)
                        try:
                            value = page.locator(selector).inner_text()
                            print("[CHECK_VALUE] -----------------------------------HO LETTO QUESTO VALORE---->", value)
                            if not(value_to_be_checked.upper().strip() in value.upper().strip()):
                                raise Exception("[CHECK_VALUE] !!!!!!!!!!!!!!!!!!!!!!! FAILURE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n Bisogna prima effettuare l'accesso a questo endpoint:"+endpoint)
                            print("[CHECK_VALUE] -->"+str(value)+"<--"+" CHECK OK -->"+endpoint_name)
                        except Exception as ex:
                            print("[CHECK_VALUE] Failure CHECK_VALUE:" + endpoint_name, " -->", selector, "---->", str(ex))

                    ## CHECK_VALUE_EXPERIMENTAL
                    if (INSTRUCTION.upper() == "CHECK_VALUE_EXPERIMENTAL"):
                        print("[CHECK_VALUE_EXPERIMENTAL] ENTRO IN CHECK_VALUE_EXPERIMENTAL ", endpoint_name)
                        selector = tokens[1].strip()
                        value_to_be_checked = tokens[2].strip()
                        print("[CHECK_VALUE_EXPERIMENTAL] selector--->" + str(selector), " endpoint-->", endpoint_name)
                        try:
                            value = page.locator(selector)
                            print("[CHECK_VALUE_EXPERIMENTAL] -----------------------------------SELECTOR PRESO--->", value," count:",value.count())
                            print("----VALORI-PRESI-----")
                            value = value.all_inner_texts()

                            print("---------FINE---------")
                            print("[CHECK_VALUE_EXPERIMENTAL] -----------------------------------VALUE LETTO--->", value)

                            #print("[CHECK_VALUE] -----------------------------------HO LETTO QUESTO VALORE---->", value)
                            if not(value_to_be_checked.upper().strip() in value.upper().strip()):
                                raise Exception("[CHECK_VALUE_EXPERIMENTAL] !!!!!!!!!!!!!!!!!!!!!!! FAILURE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n Bisogna prima effettuare l'accesso a questo endpoint:"+endpoint)
                            print("[CHECK_VALUE_EXPERIMENTAL] -->"+str(value)+"<--"+" CHECK OK -->"+endpoint_name)
                        except Exception as ex:
                            print("[CHECK_VALUE_EXPERIMENTAL] Failure CHECK_VALUE_EXPERIMENTAL:" + endpoint_name, " -->", selector, "---->", str(ex))

                    ## GET_COOKIES
                    if (INSTRUCTION.upper() == "GET_COOKIES"):
                        print("[GET COOKIES] ENTRO IN GET_COOKIES ", endpoint_name)
                        try:
                            value = browser.contexts[0].cookies(endpoint)
                            print("[GET COOKIES] HO LETTO QUESTO VALORE---->", value)
                        except Exception as ex:
                            print("[GET COOKIES] Errore durante READ" + endpoint_name, " -->", selector, "---->", str(ex))

                    ## GET_SIMILAR_SELECTOR
                    if (INSTRUCTION.upper() == "GET_SIMILAR_SELECTOR"):
                        espressione_regolare = tokens[1].strip()
                        excluding = tokens[3].strip()
                        print("[GET_SIMILAR_SELECTOR] ENTRO IN GET_SIMILAR_SELECTOR ", endpoint_name,"espressione regolare:",espressione_regolare)
                        try:
                            html_string = page.content()
                            print("LEN",len(html_string))
                            with open("outhtml.txt","w+") as f:
                                f.write(html_string)
                            time.sleep(10)
                            lista_occorrenze_non_filtrata = re.findall(espressione_regolare, html_string)
                            lista_occorrenze = []
                            for elem in lista_occorrenze_non_filtrata:
                                if (excluding in elem):
                                    continue
                                lista_occorrenze.append(elem)
                            #print("\n\n---------------------------<HTML>---------------------------------\n\n",html_string,"\n\n---------------------------</HTML>---------------------------------\n\n")
                            print("[GET_SIMILAR_SELECTOR] LISTA DI TUTTE LE OCCORRENZE---->\n", lista_occorrenze)
                            last_taken_selector = "#"+lista_occorrenze[0]
                        except Exception as ex:
                            print("[GET_SIMILAR_SELECTOR] Errore durante GET_SIMILAR_SELECTOR" + endpoint_name, " -->", selector, "---->", str(ex))



                    ## COUNT_REGEX_OCCURRENCES
                    if (INSTRUCTION.upper() == "COUNT_REGEX_OCCURRENCES"):
                        espressione_regolare = tokens[1].strip()
                        html_string = page.content()
                        with open("outhtml_count.txt", "w+") as f:
                            f.write(html_string)
                        time.sleep(10)
                        last_number_of_occurrences = len(re.findall(espressione_regolare, html_string))
                        print("[ COUNT_REGEX_OCCURRENCES_INSTAGRAM ] ", last_number_of_occurrences)


                    ## COUNT_REGEX_OCCURRENCES_INSTAGRAM
                    if (INSTRUCTION.upper() == "COUNT_REGEX_OCCURRENCES_INSTAGRAM"):
                        regex_x = tokens[1].strip()
                        regex_y = tokens[2].strip()
                        html_string = page.content()
                        with open("outhtml_count_INSTAGRAM.txt","w+") as f:
                            f.write(html_string)
                        time.sleep(10)
                        last_number_of_occurrences_row = len(re.findall(regex_x, html_string))
                        last_number_of_occurrences_column = len(re.findall(regex_y, html_string))
                        try:
                            last_number_of_occurrences_column = int(last_number_of_occurrences_column/last_number_of_occurrences_row)
                        except:
                            print("[ COUNT_REGEX_OCCURRENCES_INSTAGRAM ] ZERO OCCURRENCES FOR COLUMNS!")
                        print("[ COUNT_REGEX_OCCURRENCES_INSTAGRAM ] ",last_number_of_occurrences_row,last_number_of_occurrences_column)
                        if(instagram_step==1):
                            line = "TAKE_SELECTOR_PICTURES_INSTAGRAM------#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div > div:nth-child([PLACEHOLDER_ROW]) > div:nth-child([PLACEHOLDER_COLUMN])"
                            tokens = line.split("------")
                            INSTRUCTION = tokens[0].strip().upper()
                            instagram_step = 0

                    ## COUNT_REGEX_OCCURRENCES_INSTAGRAM_DEEP
                    if (INSTRUCTION.upper() == "COUNT_REGEX_OCCURRENCES_INSTAGRAM_DEEP"):
                        regex_x = tokens[1].strip()
                        regex_y = tokens[2].strip()
                        html_string = page.content()
                        with open("outhtml_count_INSTAGRAM.txt","w+") as f:
                            f.write(html_string)
                        time.sleep(10)
                        last_number_of_occurrences_row = len(re.findall(regex_x, html_string))
                        last_number_of_occurrences_column = len(re.findall(regex_y, html_string))
                        try:
                            last_number_of_occurrences_column = int(last_number_of_occurrences_column/last_number_of_occurrences_row)
                        except:
                            print("[ COUNT_REGEX_OCCURRENCES_INSTAGRAM_DEEP ] ZERO OCCURRENCES FOR COLUMNS!")
                        print("[ COUNT_REGEX_OCCURRENCES_INSTAGRAM_DEEP ] ",last_number_of_occurrences_row,last_number_of_occurrences_column)
                        if(instagram_step==1):
                            line = "TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP------#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div > div:nth-child([PLACEHOLDER_ROW]) > div:nth-child([PLACEHOLDER_COLUMN])"
                            tokens = line.split("------")
                            INSTRUCTION = tokens[0].strip().upper()
                            instagram_step = 0


                    ## TAKE_SELECTOR_PICTURES_INSTAGRAM
                    if (INSTRUCTION.upper() == "TAKE_SELECTOR_PICTURES_INSTAGRAM"):
                        base_string_selector = tokens[1].strip()
                        max_row = last_number_of_occurrences_row
                        max_column = last_number_of_occurrences_column
                        '''
                        try:
                            max_x = int(tokens[2].strip())
                            max_y = int(tokens[3].strip())
                        except Exception as e:
                            print("[TAKE_SELECTOR_PICTURES_INSTAGRAM] ERROR! ",str(e))
                        '''
                        for row in range(1,max_row):
                            for column in range(1,max_column):
                                current_selector = base_string_selector.replace("[PLACEHOLDER_ROW]",str(row)).replace("[PLACEHOLDER_COLUMN]",str(column))
                                print("[TAKE_SELECTOR_PICTURES_INSTAGRAM] current_selector ",current_selector)
                                page.locator(current_selector).screenshot(path=endpoint_name + "/" +chr(prefix)+"_"+"instagram_profile_"+str(row)+"_"+str(column)+".png")
                                print("[TAKE_SELECTOR_PICTURES_INSTAGRAM] JUST TAKEN ",row,column)

                    ## TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP
                    if (INSTRUCTION.upper() == "TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP"):
                        base_string_selector = tokens[1].strip()
                        max_row = last_number_of_occurrences_row
                        max_column = last_number_of_occurrences_column
                        '''
                        try:
                            max_x = int(tokens[2].strip())
                            max_y = int(tokens[3].strip())
                        except Exception as e:
                            print("[TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP] ERROR! ",str(e))
                        '''
                        for row in range(1,max_row):
                            for column in range(1,max_column):
                                current_selector = base_string_selector.replace("[PLACEHOLDER_ROW]",str(row)).replace("[PLACEHOLDER_COLUMN]",str(column))
                                print("[TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP] current_selector ",current_selector)
                                page.locator(current_selector).click()
                                time.sleep(1)
                                picture_date = page.locator("body > div.RnEpo._Yhr4 > div.pbNvD.QZZGH.bW6vo > div > article > div > div.HP0qD > div > div > div.eo2As > div.NnvRN > div > a > div > time").inner_text()
                                print("[TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP] CURRENT_TAKEN_TIME:",picture_date)
                                page.locator("body > div.RnEpo._Yhr4 > div.pbNvD.QZZGH.bW6vo > div > article > div > div._97aPb.C2dOX").screenshot(path=endpoint_name + "/"+picture_date+".png")
                                page.go_back()

                                print("[TAKE_SELECTOR_PICTURES_INSTAGRAM_DEEP] JUST TAKEN ",row,column)

                    ## COUNT_REGEX_OCCURRENCES_INSTAGRAM
                    if (INSTRUCTION.upper() == "EXIT"):
                        print("[EXIT]")
                        browser.close()
                        exit()

                browser.close()

