from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from prettytable import PrettyTable
from time import sleep
import re


# Function to set email, password, and submit the login form
def set_email_password_submit(driver, email, password):
    # Locate email field and enter email
    email_field = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div/form/div[1]/input')
    email_field.send_keys(f"{email}")

    # Locate password field and enter password
    password_field = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div/form/div[2]/div/input')
    password_field.send_keys(f"{password}")

    # Locate submit button and click it
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div/form/button')
    submit_button.click()


# Function to scrape links and bio from a given username's profile
def scrape_links_username(driver, username):
    try:
        username_url = f"https://tiktok.com/@{username}"
        driver.implicitly_wait(10)

        # Open a new tab with the provided username URL
        driver.execute_script(f"window.open('{username_url}', '_target');")

        # Wait for the new tab to open
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])

        # Wait for elements to be visible on the page
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]')))
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h2')))

        # Extract bio and links
        followers_number = driver.find_element(By.XPATH,
                                                         value='//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[2]/strong').text
        bio = driver.find_element(by=By.XPATH, value='//*[@id="main-content-others_homepage"]/div/div[1]/h2').text
        links = [bio] + [followers_number]
        return links
    except Exception:
        return 'Something went Wrong'


# Function for scrolling mechanism
def scroll_mechanism(driver, times):
    while times > 0:
        # Find the last paragraph element and perform a move_to_element action
        follower = driver.find_elements(by=By.TAG_NAME, value='p')[-1]
        actions = ActionChains(driver)
        actions.move_to_element(follower).perform()
        times -= 1
        sleep(1)


# Function for authentication mode
def auth_mode(driver):
    # Find and click the email input
    email_username = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div/div/div[1]/div[2]/div[2]')
    email_username.click()

    driver.implicitly_wait(20)
    # Click the email field
    email = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div/form/div[1]/a')
    email.click()


# Function to submit the "followers" section
def submit_followers(driver):
    driver.implicitly_wait(10)
    # Wait for the followers section to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[1]/span')))
    followers = driver.find_element(by=By.XPATH,
                                    value='//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[1]/span')
    followers.click()
    driver.implicitly_wait(10)
    sleep(4)


# Function to wait for solving captcha
def wait_to_solve_captcha(driver):
    # Wait for the header more menu icon to be clickable
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-more-menu-icon"]')))
    sleep(10)
    driver.implicitly_wait(30)
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-more-menu-icon"]')))
    sleep(5)


# Function to deserialize usernames from followers
def deserialize_usernames(followers):
    return [f.text for f in followers]


# Function to close all tabs except the current one
def close_all_except_current_tab(driver):
    # Get all tab lists and current tab
    all_tab_list = driver.window_handles
    current_tab = driver.current_window_handle

    # Print Current Tab name.
    print("Current Tab = " + driver.title)

    # Iterate over open tabs and close them except for the current one
    for window in all_tab_list:
        if window != current_tab:
            driver.switch_to.window(window)
            print("Closing Tab = " + driver.title)
            driver.close()
        sleep(1)


# Function to save data to a file
def save_to_file(data):
    with open('scraper_emails.txt', 'w', encoding='utf-8') as file:
        file.write(data + '\n')  # Add a newline after each entry


def extract_emails(text):
    # Regular expression for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all matches of the email pattern in the text
    emails = re.findall(email_pattern, text)

    return emails


# Main function
def main():
    username = input("Enter username of tiktok(ex: gwynibear_): ")
    tiktok_url = "https://www.tiktok.com/"
    email = input('Enter your email address you create Tiktok account with: ')
    password = input('Enter your password of email: ')
    MAX_USERS = 100
    SCROLL_TIMES = 5

    # Set up Chrome webdriver
    _options = webdriver.ChromeOptions()
    # Change user agent randomly for untracked
    ua = UserAgent()
    choose_user_agent = ua.random
    print('user_agent: ', choose_user_agent)
    _options.add_argument(f"--user-agent={choose_user_agent}")
    driver = webdriver.Chrome(service=Service(executable_path='./chromedriver.exe', options=_options))

    # Open TikTok website
    driver.get(tiktok_url)
    driver.implicitly_wait(20)

    # Enter authentication mode
    auth_mode(driver)

    # Set email, password, and submit the login form
    set_email_password_submit(driver, email, password)

    driver.implicitly_wait(40)

    # Wait for solving captcha
    wait_to_solve_captcha(driver)

    # Scrape links from the owner's profile
    links = scrape_links_username(driver, username)

    # Submit the "followers" section
    submit_followers(driver)

    # Scroll through the followers
    scroll_mechanism(driver, SCROLL_TIMES)

    # Wait for the followers section to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="tux-portal-container"]/div/div[2]/div/div/div[2]/div/div/section/div/div[1]')))

    # Find all paragraph elements
    find_all_ps = driver.find_elements(by=By.TAG_NAME, value='p')
    almost_following = find_all_ps[:]

    # Deserialize follower usernames
    follower_ids = deserialize_usernames(almost_following[4:])
    try:
        # Find and remove the 'Videos' element
        index_vdo = follower_ids.index('Videos')
        follower_ids = follower_ids[index_vdo + 1:]
    except Exception:
        follower_ids = follower_ids[3:]

    usernames_bio = [
        ['owner', username, links]
    ]

    # Loop through follower IDs and scrape links
    for i, follower in enumerate(follower_ids):
        print(follower, MAX_USERS, i)
        try:
            if i == MAX_USERS:
                # Close the driver if the maximum number of users is reached
                driver.close()
                break

            # Scrape links for each follower
            links = scrape_links_username(driver, follower)
            emails = ', '.join(extract_emails(links[0]))
            # Continue if no email is found in the links
            if not emails:
                continue

            # Create PrettyTable with the scraped data
            table = PrettyTable(
                field_names=['Username', 'Bio', 'Followers'],
                title=f'TikTok Scraped result: {username}'
            )
            print('sort')
            print(usernames_bio[1:])
            sort_followers = sorted(usernames_bio[1:], key=lambda x: x[-1], reverse=True)
            # Add rows to the PrettyTable
            if not sort_followers:
                table.add_row(['No email or inst (@) found'] * 3)
            else:
                table.add_rows(sort_followers)
            # Print or display the PrettyTable
            print(table)
            # Save the PrettyTable to a file
            save_to_file(table.get_string())

            # Append username, bio, and links to the usernames_bio list
            usernames_bio.append(
                [follower, emails, links[1]]
            )
        except Exception:
            MAX_USERS += 1
            continue

    # Quit the webdriver
    driver.quit()


# Entry point of the script
if __name__ == '__main__':
    main()
