import pandas as pd
import numpy as np

# All operational stations across major Delhi Metro lines
STATIONS = {
    "Yellow": [
        "Samaypur Badli", "Rohini Sector 18", "Haiderpur Badli Mor", "Jahangirpuri", 
        "Adarsh Nagar", "Azadpur", "Model Town", "GTB Nagar", "Vishwavidyalaya", 
        "Vidhan Sabha", "Civil Lines", "Kashmere Gate", "Chandni Chowk", "Chawri Bazar", 
        "New Delhi", "Rajiv Chowk", "Patel Chowk", "Central Secretariat", "Udyog Bhavan", 
        "Lok Kalyan Marg", "Jor Bagh", "INA", "AIIMS", "Green Park", "Hauz Khas", 
        "Malviya Nagar", "Saket", "Qutub Minar", "Chhattarpur", "Sultanpur", 
        "Ghitorni", "Arjangarh", "Guru Dronacharya", "Sikanderpur", "MG Road", 
        "IFFCO Chowk", "HUDA City Centre"
    ],
    "Blue": [
        "Dwarka Sector 21", "Dwarka Sector 8", "Dwarka Sector 9", "Dwarka Sector 10", 
        "Dwarka Sector 11", "Dwarka Sector 12", "Dwarka Sector 13", "Dwarka Sector 14", 
        "Dwarka", "Janakpuri West", "Janakpuri East", "Tilak Nagar", "Subhash Nagar", 
        "Tagore Garden", "Rajouri Garden", "Ramesh Nagar", "Moti Nagar", "Kirti Nagar", 
        "Shadipur", "Patel Nagar", "Rajendra Place", "Karol Bagh", "Jhandewalan", 
        "R K Ashram Marg", "Rajiv Chowk", "Barakhamba Road", "Mandi House", "Pragati Maidan", 
        "Indraprastha", "Yamuna Bank", "Akshardham", "Mayur Vihar Phase 1", "Noida Sector 15", 
        "Noida Sector 16", "Noida Sector 18", "Botanical Garden"
    ],
    "Red": [
        "Rithala", "Rohini West", "Rohini East", "Pitampura", "Kohat Enclave", 
        "Netaji Subhash Place", "Keshav Puram", "Kanhaiya Nagar", "Inderlok", 
        "Shastri Nagar", "Pratap Nagar", "Pul Bangash", "Tis Hazari", "Kashmere Gate", 
        "Shastri Park", "Seelampur", "Welcome", "Shahdara", "Mansarovar Park", 
        "Jhilmil", "Dilshad Garden", "Shaheed Sthal"
    ],
    "Green": [
        "Kirti Nagar", "Inderlok", "Ashok Park Main", "Punjabi Bagh", "Shivaji Park", 
        "Madipur", "Paschim Vihar East", "Paschim Vihar West", "Peeragarhi", 
        "Udyog Nagar", "Surajmal Stadium", "Nangloi", "Nangloi Railway Station", 
        "Rajdhani Park", "Mundka", "Mundka Industrial Area", "Ghevra", "Tikri Kalan", 
        "Tikri Border", "Pandit Shree Ram Sharma", "Bahadurgarh City", "Brig. Hoshiar Singh"
    ],
    "Violet": [
        "Kashmere Gate", "Lal Quila", "Jama Masjid", "Delhi Gate", "ITO", 
        "Mandi House", "Khan Market", "Jawaharlal Nehru Stadium", "Jangpura", "Lajpat Nagar", 
        "Moolchand", "Kailash Colony", "Nehru Place", "Kalkaji Mandir", "Govind Puri", 
        "Harkesh Nagar Okhla", "Jasola Apollo", "Sarita Vihar", "Mohan Estate", 
        "Tughlakabad", "Badarpur Border", "Sarai", "Sector 28", "Badkal Mor", 
        "Old Faridabad", "Neelam Chowk Ajronda", "Bata Chowk", "Escorts Mujesar", 
        "Sant Surdas", "Raja Nahar Singh"
    ],
    "Pink": [
        "Majlis Park", "Azadpur", "Shalimar Bagh", "Netaji Subhash Place", "Shakurpur", 
        "Punjabi Bagh West", "ESI Hospital", "Rajouri Garden", "Mayapuri", "Naraina Vihar", 
        "Delhi Cantt", "South Campus", "Moti Bagh", "Bhikaji Cama Place", 
        "Sarojini Nagar", "INA", "South Extension", "Lajpat Nagar", "Vinobapuri", 
        "Ashram", "Hazrat Nizamuddin", "Mayur Vihar Phase 1", "Mayur Vihar Pocket 1", 
        "Trilokpuri Sanjay Lake", "Vinod Nagar East", "Mandawali", "Anand Vihar", 
        "Karkarduma", "Karkarduma Court", "Krishna Nagar", "East Azad Nagar", "Welcome", 
        "Jaffrabad", "Maujpur", "Gokulkuri", "Johri Enclave", "Shiv Vihar"
    ],
    "Magenta": [
        "Janakpuri West", "Dabri Mor", "Dashrathpuri", "Palam", "Sadar Bazar Cantonment", 
        "Terminal 1-IGI Airport", "Shankar Vihar", "Vasant Vihar", "Munirka", "RK Puram", 
        "IIT", "Hauz Khas", "Panchsheel Park", "Chirag Delhi", "Greater Kailash", 
        "Nehru Enclave", "Kalkaji Mandir", "Okhla NSIC", "Sukhdev Vihar", "Jamia Millia Islamia", 
        "Okhla Vihar", "Jasola Vihar Shaheen Bagh", "Kalindi Kunj", "Okhla Bird Sanctuary", 
        "Botanical Garden"
    ]
}

# Major interchange stations mapped across the network
INTERCHANGE = {
    "Rajiv Chowk", "Kashmere Gate", "Yamuna Bank", "INA", "Hauz Khas", "Azadpur", 
    "Netaji Subhash Place", "Lajpat Nagar", "Kalkaji Mandir", "Anand Vihar", 
    "Mandi House", "Kirti Nagar", "Inderlok", "Welcome", "Janakpuri West", "Botanical Garden"
}

PEAK_HOURS = {8, 9, 10, 17, 18, 19}

np.random.seed(42)
rows = []

# Loop over 180 days, operational hours, and all populated lines/stations
for day in range(180):  
    for hour in range(5, 24):  
        for line, stations in STATIONS.items():
            for station in stations:
                is_peak = 1 if hour in PEAK_HOURS else 0
                is_weekend = 1 if day % 7 in (5, 6) else 0
                is_interchange = 1 if station in INTERCHANGE else 0
                
                # Realistic crowd simulation formula
                base = (200 + is_peak * 350 + is_interchange * 120 - is_weekend * 80 + np.sin(hour / 3) * 30)
                count = max(10, int(np.random.normal(base, 60)))
                
                if count > 480:
                    label = "High"
                elif count > 260:
                    label = "Medium"
                else:
                    label = "Low"
                    
                rows.append({
                    "station": station,
                    "line": line,
                    "hour": hour,
                    "day_of_week": day % 7,
                    "is_peak": is_peak,
                    "is_weekend": is_weekend,
                    "is_interchange": is_interchange,
                    "passenger_count": count,
                    "crowd_level": label
                })

df = pd.DataFrame(rows)
df.to_csv("data/ridership.csv", index=False)

print(f"Generated {len(df):,} rows. Sample:")
print(df.head(3).to_string())
print("\nLabel distribution:\n", df["crowd_level"].value_counts())