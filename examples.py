examples = [
    {
       "input": "Give me users who can view reports",
       "query": "SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE frontend_controller LIKE '%ReportViewing%' AND is_deleted = 0;"
    },
    {
        "input":"Give me users from Pune",
        "query":"""SELECT CONCAT(u.first_name, ' ', u.last_name) AS name 
                FROM users AS u 
                JOIN service_partner AS sp ON sp.fk_user_id = u.id
                JOIN service_partner_office AS spo ON spo.fk_sp_id = sp.service_partner_id
                JOIN city AS c ON c.city_id = spo.fk_city_id 
                WHERE c.city_name = 'Pune' AND u.is_deleted = 0 and u.type = 'SP' and u.role = 12 and u.partner_working_under = 'SCOGO'"""
    },
    {
        "input":"Give me users who can execute ticket",
        "query":"SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE frontend_controller LIKE '%TicketExecution%' AND is_deleted = 0"
    },
    {
        "input":"Give me contact details of users",
        "query":"SELECT concat(first_name,'',last_name) as Name,mobile,email from users AND is_deleted=0;"
    },
    { 
        "input": "Give me service partners from Pune",
        "query": "SELECT sp.sp_name AS name, u.mobile AS contact_number, u.email FROM service_partner AS sp JOIN service_partner_office AS spo ON sp.service_partner_id = spo.fk_sp_id JOIN city AS c ON spo.fk_city_id = c.city_id JOIN users AS u ON sp.fk_user_id = u.id WHERE c.city_name = 'Pune' AND sp.is_deleted = 0 AND spo.is_deleted = 0 AND u.is_deleted = 0 and u.type = 'SP' and u.role = 12 and u.partner_working_under = 'SCOGO';"
    },
    {
        "input": "Which cities have service partners?",
        "query" : "SELECT DISTINCT c.city_name FROM users as u join service_partner as sp on sp.fk_user_id = u.id join service_partner_office as spo on spo.fk_sp_id = sp.service_partner_id join city as c on c.city_id = spo.fk_city_id WHERE spo.is_deleted = 0 AND sp.is_deleted = 0 AND u.is_deleted = 0 and u.type = 'SP' and u.role = 12 and u.partner_working_under = 'SCOGO';"
    },
    {
        "input": "How many clusters do we have?",
        "query" : "SELECT count(*) from users where type = 'CLUSTER' and is_deleted = 0"
    },
    {
        "input": "How many tickets are completed for lavelle?",
        "query": "select count(t.id) from tickets as t join customers as c on c.customer_id = t.fk_customer_id where c.customer_company_name like '%lavelle%' and t.is_deleted=0 and c.is_deleted = 0 and (t.is_sign_off_request = 1 or t.closed_by_noc != 0)"
    },
    {
        "input": "How many tickets are completed by nazre?",
        "query": "select count(t.id) from tickets as t join users as u on u.id = t.accepted_sp_id where u.first_name like '%nazre%' and t.is_deleted=0 and c=u.is_deleted = 0 and (t.is_sign_off_request = 1 or t.closed_by_noc != 0)"
    },
    {
        "input": "Give me the total Incentive earning of nazre in last one month.",
        "query": "SELECT CONCAT(u.first_name, ' ', u.last_name) AS 'user',COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive', COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Additional Incentive', COALESCE(basic_incentive.positiveSum, 0) + COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Total Incentive' FROM users AS u LEFT JOIN (SELECT fk_user_id, COALESCE(SUM(orderAmount), 0) AS positiveSum FROM wallet_transaction WHERE paymentType = 'INCENTIVE' AND is_deleted = 0 AND status not in ('Pending','Failed') AND txTime > DATE_SUB(NOW(), INTERVAL 1 MONTH) GROUP BY fk_user_id) AS basic_incentive ON basic_incentive.fk_user_id = u.id LEFT JOIN (SELECT fk_user_id, COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum, COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum FROM wallet_transaction WHERE paymentType = 'WALLET_TRANSFER' AND is_deleted = 0 AND status not in ('Pending','Failed') AND reason = 'INCENTIVE' AND processed_at > DATE_SUB(NOW(), INTERVAL 1 MONTH) GROUP BY fk_user_id) AS additional_incentive ON additional_incentive.fk_user_id = u.id WHERE u.is_deleted = 0 AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%nazre%')"
    },
    {
        "input": "Provide me the total Incentive earning of mehul in last two month.",
        "query": "SELECT CONCAT(u.first_name, ' ', u.last_name) AS 'user',COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive', COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Additional Incentive', COALESCE(basic_incentive.positiveSum, 0) + COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Total Incentive' FROM users AS u LEFT JOIN (SELECT fk_user_id, COALESCE(SUM(orderAmount), 0) AS positiveSum FROM wallet_transaction WHERE paymentType = 'INCENTIVE' AND is_deleted = 0 AND status not in ('Pending','Failed') AND txTime > DATE_SUB(NOW(), INTERVAL 2 MONTH) GROUP BY fk_user_id) AS basic_incentive ON basic_incentive.fk_user_id = u.id LEFT JOIN (SELECT fk_user_id, COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum, COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum FROM wallet_transaction WHERE paymentType = 'WALLET_TRANSFER' AND is_deleted = 0 AND status not in ('Pending','Failed') AND reason = 'INCENTIVE' AND processed_at > DATE_SUB(NOW(), INTERVAL 2 MONTH) GROUP BY fk_user_id) AS additional_incentive ON additional_incentive.fk_user_id = u.id WHERE u.is_deleted = 0 AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%mehul%')"
    },
    {
        "input" : "Total Incentive earnings of Nazre in July 2024.",
        "query": """SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS 'user',
            COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
            COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Additional Incentive',
            COALESCE(basic_incentive.positiveSum, 0) + COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Total Incentive'
        FROM 
            users AS u
        LEFT JOIN 
            (SELECT fk_user_id, COALESCE(SUM(orderAmount), 0) AS positiveSum 
            FROM wallet_transaction 
            WHERE paymentType = 'INCENTIVE' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending','Failed') 
            AND txTime BETWEEN '2024-07-01' AND '2024-07-31'
            GROUP BY fk_user_id) AS basic_incentive 
        ON 
            basic_incentive.fk_user_id = u.id
        LEFT JOIN 
            (SELECT fk_user_id, 
                    COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
                    COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum 
            FROM wallet_transaction 
            WHERE paymentType = 'WALLET_TRANSFER' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending','Failed') 
            AND reason = 'INCENTIVE' 
            AND processed_at BETWEEN '2024-07-01' AND '2024-07-31'
            GROUP BY fk_user_id) AS additional_incentive 
        ON 
            additional_incentive.fk_user_id = u.id
        WHERE 
            u.is_deleted = 0 
            AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%nazre%'); """
    },
    {
        "input" : "Incentive earnings of Mehul from 25th July 2024 to 6th August 2024",
        "query" : """SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS 'user',
            COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
            COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Additional Incentive',
            COALESCE(basic_incentive.positiveSum, 0) + COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Total Incentive'
        FROM 
            users AS u
        LEFT JOIN 
            (SELECT fk_user_id, COALESCE(SUM(orderAmount), 0) AS positiveSum 
            FROM wallet_transaction 
            WHERE paymentType = 'INCENTIVE' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending','Failed') 
            AND txTime BETWEEN '2024-07-25' AND '2024-08-06'
            GROUP BY fk_user_id) AS basic_incentive 
        ON 
            basic_incentive.fk_user_id = u.id
        LEFT JOIN 
            (SELECT fk_user_id, 
                    COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
                    COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum 
            FROM wallet_transaction 
            WHERE paymentType = 'WALLET_TRANSFER' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending','Failed') 
            AND reason = 'INCENTIVE' 
            AND processed_at BETWEEN '2024-07-25' AND '2024-08-06'
            GROUP BY fk_user_id) AS additional_incentive 
        ON 
            additional_incentive.fk_user_id = u.id
        WHERE 
            u.is_deleted = 0 
            AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%mehul%'); """
},
{
    "input" : "Total earnings of Nazre from 25th July 2024 to 6th August 2024 ",
    "query" : """SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS 'user',
            COALESCE(basic_earning.positiveSum, 0) AS 'Base Service Earning',
            COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
            COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Additional Income',
            COALESCE(basic_earning.positiveSum, 0) + COALESCE(basic_incentive.positiveSum, 0) + 
            COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Total Earning'
        FROM 
            users AS u
        LEFT JOIN 
            (SELECT 
                fk_sp_id, 
                COALESCE(SUM(amount), 0) AS positiveSum 
            FROM 
                payment_transactions 
            WHERE 
                is_deleted = 0 
                AND is_request_raised IN (2, 4) 
                AND due_date BETWEEN '2023-07-01' AND '2023-07-31' 
            GROUP BY 
                fk_sp_id
            ) AS basic_earning 
        ON 
            basic_earning.fk_sp_id = u.id
        LEFT JOIN 
            (SELECT 
                fk_user_id, 
                COALESCE(SUM(orderAmount), 0) AS positiveSum
            FROM 
                wallet_transaction 
            WHERE 
                paymentType = 'INCENTIVE' 
                AND is_deleted = 0 
                AND status NOT IN ('Pending', 'Failed') 
                AND txTime BETWEEN '2024-07-25' AND '2024-08-06' 
            GROUP BY 
                fk_user_id
            ) AS basic_incentive 
        ON 
            basic_incentive.fk_user_id = u.id
        LEFT JOIN 
            (SELECT 
                fk_user_id, 
                COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
                COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum
            FROM 
                wallet_transaction 
            WHERE 
                paymentType = 'WALLET_TRANSFER' 
                AND is_deleted = 0 
                AND status NOT IN ('Pending', 'Failed') 
                AND reason IN ('SERVICE', 'TRAVEL', 'MATERIAL', 'COURIER', 'INCENTIVE') 
                AND processed_at BETWEEN '2024-07-25' AND '2024-08-06' 
            GROUP BY 
                fk_user_id
            ) AS additional_income 
        ON 
            additional_income.fk_user_id = u.id
        WHERE 
            u.is_deleted = 0 
            AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%nazre%');"""
},
{
    "input" : "give me project wise count of tickets we have completed for bolt",
    "query" : """SELECT p.project_name, COUNT(t.id) AS completed_tickets
                FROM projects p
                JOIN tickets t ON p.id = t.fk_project_id
                JOIN customers c ON p.fk_customer_id = c.customer_id
                WHERE c.customer_company_name LIKE '%bolt%' AND t.is_sign_off_request = 1
                GROUP BY p.project_name"""
},
{
    "input" : "give me project wise count of tickets we have completed for lavelle",
    "query" : """SELECT p.project_name, COUNT(t.id) AS completed_tickets
                FROM projects p
                JOIN tickets t ON p.id = t.fk_project_id
                JOIN customers c ON p.fk_customer_id = c.customer_id
                WHERE c.customer_company_name LIKE '%lavelle%' AND t.is_sign_off_request = 1
                GROUP BY p.project_name"""
},
{
    "input" : "Total earnings of taiyab in July 2024 ",
    "query" : """SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS 'user',
            COALESCE(basic_earning.positiveSum, 0) AS 'Base Service Earning',
            COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
            COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Additional Income',
            COALESCE(basic_earning.positiveSum, 0) + COALESCE(basic_incentive.positiveSum, 0) + 
            COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Total Earning'
        FROM 
            users AS u
        LEFT JOIN 
            (SELECT 
                fk_sp_id, 
                COALESCE(SUM(amount), 0) AS positiveSum 
            FROM 
                payment_transactions 
            WHERE 
                is_deleted = 0 
                AND is_request_raised IN (2, 4) 
                AND due_date BETWEEN '2023-07-01' AND '2023-07-31' 
            GROUP BY 
                fk_sp_id
            ) AS basic_earning 
        ON 
            basic_earning.fk_sp_id = u.id
        LEFT JOIN 
            (SELECT 
                fk_user_id, 
                COALESCE(SUM(orderAmount), 0) AS positiveSum
            FROM 
                wallet_transaction 
            WHERE 
                paymentType = 'INCENTIVE' 
                AND is_deleted = 0 
                AND status NOT IN ('Pending', 'Failed') 
                AND txTime BETWEEN '2024-07-01' AND '2024-07-31' 
            GROUP BY 
                fk_user_id
            ) AS basic_incentive 
        ON 
            basic_incentive.fk_user_id = u.id
        LEFT JOIN 
            (SELECT 
                fk_user_id, 
                COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
                COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum
            FROM 
                wallet_transaction 
            WHERE 
                paymentType = 'WALLET_TRANSFER' 
                AND is_deleted = 0 
                AND status NOT IN ('Pending', 'Failed') 
                AND reason IN ('SERVICE', 'TRAVEL', 'MATERIAL', 'COURIER', 'INCENTIVE') 
                AND processed_at BETWEEN '2024-07-01' AND '2024-07-31' 
            GROUP BY 
                fk_user_id
            ) AS additional_income 
        ON 
            additional_income.fk_user_id = u.id
        WHERE 
            u.is_deleted = 0 
            AND u.id IN (SELECT id FROM users WHERE first_name LIKE '%taiyab%')"""
},
{
    "input" : "Total earnings of john in last one month",
    "query" : """SELECT 
        CONCAT(u.first_name, ' ', u.last_name) AS 'user',
        COALESCE(basic_earning.positiveSum, 0) AS 'Base Service Earning',
        COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
        COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Additional Income',
        COALESCE(basic_earning.positiveSum, 0) + COALESCE(basic_incentive.positiveSum, 0) + 
        COALESCE(additional_income.positiveSum, 0) + COALESCE(additional_income.negativeSum, 0) AS 'Total Earning'
    FROM 
        users AS u
    LEFT JOIN 
        (SELECT 
            fk_sp_id, 
            COALESCE(SUM(amount), 0) AS positiveSum 
        FROM 
            payment_transactions 
        WHERE 
            is_deleted = 0 
            AND is_request_raised IN (2, 4) 
            AND due_date > DATE_SUB(NOW(), INTERVAL 1 MONTH) 
        GROUP BY 
            fk_sp_id
        ) AS basic_earning 
    ON 
        basic_earning.fk_sp_id = u.id
    LEFT JOIN 
        (SELECT 
            fk_user_id, 
            COALESCE(SUM(orderAmount), 0) AS positiveSum
        FROM 
            wallet_transaction 
        WHERE 
            paymentType = 'INCENTIVE' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending', 'Failed') 
            AND txTime > DATE_SUB(NOW(), INTERVAL 1 MONTH) 
        GROUP BY 
            fk_user_id
        ) AS basic_incentive 
    ON 
        basic_incentive.fk_user_id = u.id
    LEFT JOIN 
        (SELECT 
            fk_user_id, 
            COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
            COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum
        FROM 
            wallet_transaction 
        WHERE 
            paymentType = 'WALLET_TRANSFER' 
            AND is_deleted = 0 
            AND status NOT IN ('Pending', 'Failed') 
            AND reason IN ('SERVICE', 'TRAVEL', 'MATERIAL', 'COURIER', 'INCENTIVE') 
            AND processed_at > DATE_SUB(NOW(), INTERVAL 1 MONTH) 
        GROUP BY 
            fk_user_id
        ) AS additional_income 
    ON 
        additional_income.fk_user_id = u.id
    WHERE 
        u.is_deleted = 0 
        AND u.first_name LIKE '%john%' """
},
{
    "input" : "Total Incentive earnings of john in last 2 months.",
    "query" : """SELECT 
        CONCAT(u.first_name, ' ', u.last_name) AS 'user',
        COALESCE(basic_incentive.positiveSum, 0) AS 'Base Incentive',
        COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Additional Incentive',
        COALESCE(basic_incentive.positiveSum, 0) + COALESCE(additional_incentive.positiveSum, 0) + COALESCE(additional_incentive.negativeSum, 0) AS 'Total Incentive'
    FROM 
        users AS u
    LEFT JOIN 
        (SELECT fk_user_id, COALESCE(SUM(orderAmount), 0) AS positiveSum 
        FROM wallet_transaction 
        WHERE paymentType = 'INCENTIVE' 
        AND is_deleted = 0 
        AND status NOT IN ('Pending', 'Failed') 
        AND txTime > DATE_SUB(NOW(), INTERVAL 2 MONTH)
        GROUP BY fk_user_id) AS basic_incentive 
    ON 
        basic_incentive.fk_user_id = u.id
    LEFT JOIN 
        (SELECT fk_user_id, 
                COALESCE(SUM(CASE WHEN fk_user_id = recepient THEN orderAmount ELSE 0 END), 0) AS positiveSum,
                COALESCE(SUM(CASE WHEN fk_user_id = sender THEN orderAmount ELSE 0 END) * -1, 0) AS negativeSum 
        FROM wallet_transaction 
        WHERE paymentType = 'WALLET_TRANSFER' 
        AND is_deleted = 0 
        AND status NOT IN ('Pending', 'Failed') 
        AND reason = 'INCENTIVE' 
        AND processed_at > DATE_SUB(NOW(), INTERVAL 2 MONTH)
        GROUP BY fk_user_id) AS additional_incentive 
    ON 
        additional_incentive.fk_user_id = u.id
    WHERE 
        u.is_deleted = 0 
        AND u.first_name LIKE '%john%'"""
},
{
    "input" : "Give me my vendors from Pune.",
    "query" : """SELECT 
        sp.sp_name AS name, u.mobile AS contact_number, u.email 
        FROM service_partner AS sp 
        JOIN service_partner_office AS spo ON sp.service_partner_id = spo.fk_sp_id 
        JOIN city AS c ON spo.fk_city_id = c.city_id 
        JOIN users AS u ON sp.fk_user_id = u.id 
        JOIN service_partner_under_customer AS spuc ON sp.service_partner_id = spuc.fk_service_partner_id 
        WHERE c.city_name = 'Pune' AND spuc.fk_customer_id = 209 AND sp.is_deleted = 0 AND spo.is_deleted = 0 AND u.is_deleted = 0 and u.type = 'SP' and u.role = 12 and u.partner_working_under = 'CUSTOMER';"""
},
{
    "input" : "Tickets completed in June 2024",
    "query" : """SELECT id, site_completed_on
            FROM tickets
            WHERE is_sign_off_request = 1
                    AND is_escalated = 0
                    AND site_completed_on BETWEEN '2024-06-01' AND '2024-06-30'
                    AND fk_customer_id = 209"""
},
{
    "input" : 'Todays planned ticket',
    "query" : 'SELECT id, job_ticket_number, execution_date FROM tickets WHERE DATE(execution_date) = CURDATE() AND is_deleted = 0 and request_raised = 1'
},
{
    "input" : 'count of todays planned ticket',
    "query" : 'SELECT count(*) FROM tickets WHERE DATE(execution_date) = CURDATE() AND is_deleted = 0 and request_raised = 1'
}
]

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import AzureOpenAIEmbeddings
import json
import streamlit as st
import chromadb.api

chromadb.api.client.SharedSystemClient.clear_system_cache()

# Load environment variables
load_dotenv()

LIKED_PAIRS_FILE = "liked_pairs.json"

def load_liked_pairs():
    """Load liked pairs from the JSON file."""
    if os.path.exists(LIKED_PAIRS_FILE):
        try:
            with open(LIKED_PAIRS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, return an empty list and reset the file
            return []
    return []

def save_liked_answer_to_examples(input_text, query):
    liked_pair = {
        "input": input_text,
        "query": query
    }
    print(liked_pair)
    # Check if the JSON file exists
    if os.path.exists(LIKED_PAIRS_FILE):
        # Load existing data
        with open(LIKED_PAIRS_FILE, "r") as f:
            liked_answers = json.load(f)
    else:
        liked_answers = []

    # Add the new liked pair
    liked_answers.append(liked_pair)

    # Save back to the JSON file
    with open(LIKED_PAIRS_FILE, "w") as f:
        json.dump(liked_answers, f, indent=4)

    print(f"Saved liked pair: {liked_pair}")

liked_pairs = load_liked_pairs()

examples = examples + liked_pairs

embed_model = AzureOpenAIEmbeddings(
    openai_api_version="2023-05-15",
    base_url=os.getenv("AOAI_ADA_BASE_URL"),
    openai_api_key=os.getenv("AOAI_ADA_KEY"),
)

def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embed_model,
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector

example_selector = get_example_selector()



