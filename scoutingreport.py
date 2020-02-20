from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

my_name = "Michael Khalil"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("./chromedriver", chrome_options = chrome_options)
def get_table_on_lifter(name):
  name_xpath = "/html/body/ul/li[2]"
  driver.get("http://www.usapl.liftingdatabase.com")
  wait = WebDriverWait(driver, 15)
  searchbox = driver.find_element_by_id("search")
  searchbox.send_keys(_convert(name))
  try:
      wait.until(EC.presence_of_element_located((By.XPATH, name_xpath)))
      wait.until(EC.element_to_be_clickable((By.XPATH, name_xpath))).click()
  except TimeoutException:
      print("Couldn't find lifter:\t" + name)
      raise NameError("Couldn't find lifter:\t" + name)
  tables = driver.find_elements_by_id("competition_view_results")
  table_elements = []
  for table in tables:
      table_elements.extend(table.find_elements_by_tag_name("tr"))

  return generate_lifter_table(table_elements)

def _convert(param):
    if isinstance(param, str):
        return param.decode('utf-8')
    else:
        return param

def generate_lifter_table(table_elements):
  lifter_table = []
  tags = ['Date', 'Competition', 'Placing',
          'Division', 'Weight Class', 'Weight',
          'Squat1', 'Squat2', 'Squat3',
          'Bench press1', 'Bench press2', 'Bench press3',
          'Deadlift1', 'Deadlift2', 'Deadlift3',
          'Total', 'Points']
  for tr in table_elements:
      cells = tr.find_elements_by_tag_name("td")
      competition_row = {}
      for (tag, td) in zip(tags, cells):
          competition_row[tag] = td.text
      lifter_table.append(competition_row)
  return lifter_table 



def get_best_numbers(lifter_table):
    best_lifts = {}
    best_total = 0
    lifts = ["Squat", "Bench press", "Deadlift"]
    best_lift = [0, 0, 0]
    best_attempt = [0, 0, 0]

    for row in lifter_table:
        if len(row.keys()) != 0:
            if float(row['Total']) > best_total:
                best_total = float(row['Total'])
            for lift in lifts:
                successes = []
                fails = []
                for i in range(1,4):
                    try:
                        attempt = float(row[lift + str(i)])
                        if attempt >= 0:
                            successes.append(attempt)
                        elif attempt < 0:
                            fails.append(attempt)
                    except ValueError:
                        idk = 1
                use_best_lift(best_lift, successes, lifts.index(lift))
                use_best_lift(best_attempt, [abs(f) for f in fails], lifts.index(lift))

    best_lifts['Total'] = best_total
    best_lifts['H-Total'] = sum(best_lift)
    best_lifts["P-Total"] = sum([max(missed, lifted) for (missed, lifted) in zip(best_lift, best_attempt)])
    for (lift, i) in zip(lifts, range(3)):
        best_lifts[lift] = best_lift[i]
        best_lifts["BF-" + lift] = best_attempt[i]
    return best_lifts

def use_best_lift(former_bests, attempts, lift_index):
    if len(attempts) > 0:
        attempt = max(attempts)
        if attempt > former_bests[lift_index]:
            former_bests[lift_index] = attempt


#print(get_best_numbers(get_table_on_lifter(my_name)))
