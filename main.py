import time
from datetime import datetime, timedelta
import random

# --- CONFIGURATION AND MOCK DATA ---
# NOTE: In a real-world scenario, you would install the 'requests' library (pip install requests)
# and use it to perform the API calls. For this environment, we simulate the network interaction.

class Config:
    """Holds all major configuration parameters."""
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
    # IMPORTANT: Replace this with your actual Gemini API Key for live planning
    API_KEY = "AIzaSyAWigcfc9bTT8HZrUl1P0anXhUlHF8pnEE" # Your key would go here
    INITIAL_BUDGET_CAD = 400.00
    TARGET_END_DATE = datetime(2025, 12, 16)
    PREPAID_PHONE_COST = 45.00
    ETH_START_PRICE_USD = 4000.00 # Placeholder price from initial Google search
    # Philosophical Vectorization Constant (Used to ensure '100% pinch' in profit calculation)
    # A positive pressure ensures directional truth (True True is truer than one True)
    PRESSURIZED_VECTOR = 1.05 # 5% profit margin base for TP calculation

    @staticmethod
    def get_user_constraints():
        """Returns the detailed user constraints for the Gemini prompt."""
        return {
            "Budget": f"${Config.INITIAL_BUDGET_CAD:.2f} CAD until {Config.TARGET_END_DATE.strftime('%B %d')}",
            "Fixed_Cost": f"Freedom Mobile prepaid: ${Config.PREPAID_PHONE_COST:.2f}",
            "Location": "Vancouver, exploring Tri-Cities, Burnaby, and Port Moody.",
            "Diet_Preferences": "No alcohol. Budget for cannabis/weed and hydration. Likes Dollarama and grocery store pastries.",
            "Meal_Tickets": "Gathering Place and Evelynne Saller meal tickets (must be prioritized for cheap meals).",
            "Schedule_Habits": "Fixed times for Coding, Meals, and Sleep. Priority on free parks/activities."
        }

# --- ETHEREUM TRACKER SIMULATION ---

class EthereumTracker:
    """
    Simulates a live Ethereum price feed and calculates Take Profit/Stop Loss
    targets based on a high-value, pressurized vectorization strategy.
    The logic implements the 'grid by 3 hours' requirement.
    """
    def __init__(self, master, start_price):
        self.current_price = start_price
        self.master = master
        self.frame = ttk.LabelFrame(master, text="ETH Perpetuals Trust Wallet Swap Tracker (USD)", padding="10 5 10 5")
        self.frame.pack(fill='x', pady=5, padx=10)

        # Labels
        self.price_label = tk.Label(self.frame, text="Loading...", font=('Inter', 14, 'bold'), fg='#3B82F6')
        self.price_label.pack(side=tk.LEFT, padx=10)

        self.tp_label = tk.Label(self.frame, text="TP: N/A", font=('Inter', 10), fg='#10B981')
        self.tp_label.pack(side=tk.LEFT, padx=10)

        self.sl_label = tk.Label(self.frame, text="SL: N/A", font=('Inter', 10), fg='#EF4444')
        self.sl_label.pack(side=tk.LEFT, padx=10)

        self.grid_label = tk.Label(self.frame, text="Grid Hours: 0 / 3", font=('Inter', 8, 'italic'))
        self.grid_label.pack(side=tk.RIGHT, padx=10)

        self.last_update_time = time.time()
        self.update_price()

    def calculate_levels(self):
        """Calculates TP/SL based on the current price and the pressurized vector."""
        # 'Minimum 100% pinch' translation: Aim for a 5% positive vector on current price for TP.
        take_profit = self.current_price * Config.PRESSURIZED_VECTOR
        # SL logic: A 'False False is a True that is True' suggests a low-risk buffer. Use a 2% buffer.
        stop_loss = self.current_price * 0.98
        return take_profit, stop_loss

    def update_price(self):
        """Simulates price update and schedules the next update."""
        time_elapsed = time.time() - self.last_update_time
        
        # 3-Hour Grid Logic: Reset price volatility every 3 simulated hours
        grid_hours = int(time_elapsed / 3600) % 3

        # Simulate small, realistic market fluctuation (random walk)
        volatility = 0.005 # 0.5% daily volatility mock
        price_change = self.current_price * volatility * (random.random() - 0.5) * 2
        self.current_price += price_change

        # Recalculate TP/SL
        tp, sl = self.calculate_levels()

        # Update GUI
        self.price_label.config(text=f"ETH Price: ${self.current_price:,.2f}")
        self.tp_label.config(text=f"TP (5% Vector): ${tp:,.2f}")
        self.sl_label.config(text=f"SL (2% Buffer): ${sl:,.2f}")
        self.grid_label.config(text=f"Grid Hours: {grid_hours} / 3")

        # Schedule the next update (e.g., every 5 seconds for a dynamic feel)
        self.master.after(5000, self.update_price)


# --- GEMINI BUDGET MENTOR CORE LOGIC ---

class BudgetMentor:
    """Handles all budgeting calculations and API interaction logic."""
    def __init__(self, app):
        self.app = app
        self.start_date = datetime.now()
        self.end_date = Config.TARGET_END_DATE
        self.total_days = (self.end_date - self.start_date).days
        self.budget_remaining = Config.INITIAL_BUDGET_CAD - Config.PREPAID_PHONE_COST
        self.daily_budget = self.budget_remaining / self.total_days if self.total_days > 0 else 0
        
        # Mock data for the 3-day lookahead and calendar
        self.current_schedule = self._generate_mock_schedule()

    def get_budget_summary(self):
        """Calculates and returns the current financial summary."""
        summary = {
            "Total_Budget": f"${Config.INITIAL_BUDGET_CAD:.2f} CAD",
            "Fixed_Cost": f"-${Config.PREPAID_PHONE_COST:.2f} (Freedom Mobile)",
            "Available_Budget": f"${self.budget_remaining:.2f} CAD",
            "Days_Remaining": f"{self.total_days} days (until {self.end_date.strftime('%B %d, %Y')})",
            "Daily_Target": f"${self.daily_budget:.2f} CAD",
            "Target_Weed_Budget": f"${self.budget_remaining * 0.15:.2f} (15% of remaining budget)",
        }
        return summary

    def _generate_mock_schedule(self):
        """
        Mocks the complex, Gemini-generated schedule based on user constraints.
        This structured data reflects the expected JSON output from the Gemini API.
        """
        return {
            (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'): {
                "day": (datetime.now() + timedelta(days=i)).strftime('%A'),
                "daily_budget_allocation": f"${self.daily_budget:.2f}",
                "activities": [
                    {
                        "time": "08:00",
                        "event": "Wake, Hydration, Prepare for Day",
                        "cost": 0.00
                    },
                    {
                        "time": "08:30",
                        "event": "Gathering Place Breakfast Ticket",
                        "location": "Gathering Place Community Centre, Vancouver",
                        "menu": "Coffee/Tea & Toast/Cereal",
                        "cost": 0.00
                    },
                    {
                        "time": "10:00",
                        "event": "Coding Session (Focus on Python GUI)",
                        "location": "Home Office/Local Library",
                        "cost": 0.00
                    },
                    {
                        "time": "12:30",
                        "event": "Grocery Store Pastry/Dollarama Snack",
                        "location": "T&T Supermarket Bakery, Vancouver",
                        "menu": "1 Cheap Pastry & Water Bottle Refill",
                        "cost": 3.50
                    },
                    {
                        "time": "14:00",
                        "event": f"***_Exploration: Rocky Point Park, Port Moody_***",
                        "location": "2800 Murray St, Port Moody",
                        "menu": "Walk the shoreline, enjoy the views (Free)",
                        "cost": 0.00
                    },
                    {
                        "time": "17:00",
                        "event": "Weed/Relaxation Break & Hydration",
                        "location": "Park/Home",
                        "cost": 5.00 # Allocation for daily consumption
                    },
                    {
                        "time": "18:30",
                        "event": "Evelynne Saller Dinner Ticket",
                        "location": "Evelynne Saller Centre, Downtown Eastside, Vancouver",
                        "menu": "Subsidized Hot Meal",
                        "cost": 0.00
                    },
                    {
                        "time": "20:00",
                        "event": "Evening Coding/Project Work",
                        "cost": 0.00
                    },
                    {
                        "time": "22:30",
                        "event": "Prepare for Sleep",
                        "cost": 0.00
                    },
                    {
                        "time": "23:00",
                        "event": "Sleep",
                        "cost": 0.00
                    }
                ],
                "daily_total_spent": 8.50, # 3.50 + 5.00
                "daily_remaining": self.daily_budget - 8.50
            } for i in range(15) # Generate a 15-day mock schedule
        }

    def _call_gemini_budget_mentor(self):
        """
        Mocks the POST request to the Gemini API with the user's detailed constraints.
        The system instructions and payload are precisely designed to meet the request
        for a 'decisive algorithmic abstract asker'.
        """
        # This function would use the 'requests' library in a real environment
        # import requests

        system_prompt = (
            "You are a highly analytical and empathetic Canadian financial mentor specializing in budget optimization "
            "for the Vancouver, BC area. Your task is to generate a structured daily itinerary and budget plan. "
            "You must prioritize free activities, utilize provided meal tickets, and adhere to all user-defined constraints. "
            "Your response must be a valid JSON object following the provided schema, detailing precise times, locations, "
            "menu items, and costs, with a mandatory distinction between essential events and highly recommended/major events "
            "by using markdown formatting (italic, bold, underline)."
        )

        user_query = (
            f"Generate a detailed 15-day itinerary starting tomorrow, based on the following: "
            f"Budget: ${self.daily_budget:.2f} CAD per day. "
            f"Constraints: {Config.get_user_constraints()}. "
            f"Output must include: daily budget allocation, meal plan (using meal tickets first, then cheap options like Dollarama/pastries), "
            f"a free activity/park with address (Vancouver, Richmond, Burnaby, Tri-Cities/Port Moody priority), and specific, fixed timings "
            f"for coding sessions, meals, and sleep."
        )

        # The actual API payload structure for a JSON response
        payload = {
            "contents": [{ "parts": [{ "text": user_query }] }],
            "systemInstruction": { "parts": [{ "text": system_prompt }] },
            "generationConfig": {
                "responseMimeType": "application/json",
                # Response schema would be complex to define here, but it would match the structure of _generate_mock_schedule
            },
        }

        # --- MOCK API CALL (For Demonstration) ---
        print("MOCK: Sending complex prompt to Gemini API...")
        time.sleep(1)
        
        # Return the mock data
        self.current_schedule = self._generate_mock_schedule()
        return "Budget plan successfully updated by Gemini AI.", self.current_schedule

    def update_schedule(self):
        """Triggers the Gemini update and refreshes the GUI."""
        try:
            message, new_schedule = self._call_gemini_budget_mentor()
            self.app.calendar_view.load_schedule(new_schedule)
            messagebox.showinfo("Gemini Update Success", message)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get budget plan: {e}")


# --- CALENDAR AND GUI VISUALIZATION ---

class CalendarView(tk.Frame):
    """A Frame to display the calendar and the 3-day lookahead."""
    def __init__(self, master):
        super().__init__(master, padx=10, pady=10, bg='#F3F4F6')
        self.pack(fill='both', expand=True)
        self.schedule_data = {}

        # Title
        tk.Label(self, text="Monthly Budgeting Calendar & Mentor Summary",
                 font=('Inter', 18, 'bold'), fg='#1F2937', bg='#F3F4F6').pack(pady=(0, 10))
        
        # Calendar Area (Main Display)
        self.calendar_frame = ttk.LabelFrame(self, text=f"Year {datetime.now().year} in Circumference", padding="10")
        self.calendar_frame.pack(fill='x', pady=10)
        self.calendar_text = scrolledtext.ScrolledText(self.calendar_frame, wrap=tk.WORD, height=15, font=('Inter', 10), relief=tk.FLAT, padx=10, pady=10)
        self.calendar_text.pack(fill='both', expand=True)
        self._setup_calendar_tags()

        # 3-Day Lookahead (Fortune of Valued Details)
        self.lookahead_frame = ttk.LabelFrame(self, text="Daily Update: Next 3-Day Fortune", padding="10")
        self.lookahead_frame.pack(fill='x', pady=10)
        self.lookahead_text = tk.Label(self.lookahead_frame, text="Awaiting Gemini Plan...", justify=tk.LEFT, anchor='w', bg='white', wraplength=700)
        self.lookahead_text.pack(fill='x', padx=5, pady=5)
        
        self.update_daily_lookahead() # Initial update

    def _setup_calendar_tags(self):
        """Sets up special formatting tags for the calendar text area."""
        self.calendar_text.tag_configure('header', font=('Inter', 12, 'bold'), foreground='#4B5563')
        # Tag for major events: italic, bold, underline
        self.calendar_text.tag_configure('major_event', font=('Inter', 10, 'bold italic underline'), foreground='#9D174D')
        self.calendar_text.tag_configure('normal', font=('Inter', 10), foreground='#374151')

    def load_schedule(self, schedule_data):
        """Loads and formats the schedule data into the calendar view."""
        self.schedule_data = schedule_data
        self.calendar_text.delete(1.0, tk.END)

        for date_str, daily_plan in schedule_data.items():
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Day Header
            self.calendar_text.insert(tk.END, f"\n--- {date_obj.strftime('%A, %B %d, %Y')} ---\n", 'header')
            self.calendar_text.insert(tk.END, f"  [Budget Target: {daily_plan['daily_budget_allocation']} | Actual Spend: ${daily_plan['daily_total_spent']:.2f}]\n", 'normal')
            
            # Events
            for activity in daily_plan['activities']:
                is_major = '***' in activity['event']
                
                # Format the detailed entry
                event_detail = (
                    f"    [{activity['time']}] {activity['event'].replace('***_', '').replace('_***', '')}\n"
                    f"      > Loc: {activity.get('location', 'N/A')}\n"
                    f"      > Menu: {activity.get('menu', 'N/A')}\n"
                    f"      > Cost: ${activity.get('cost', 0.00):.2f}\n"
                )
                
                tag = 'major_event' if is_major else 'normal'
                self.calendar_text.insert(tk.END, event_detail, tag)
        
        self.update_daily_lookahead()

    def update_daily_lookahead(self):
        """Updates the 3-day lookahead section."""
        today = datetime.now()
        lookahead_summary = ""

        if not self.schedule_data:
            self.lookahead_text.config(text="Awaiting Gemini Plan. Click 'Generate/Update Plan' below!")
            self.after(60000, self.update_daily_lookahead) # Retry in 1 minute
            return

        for i in range(1, 4): # Next 3 days (1, 2, 3)
            future_date = today + timedelta(days=i)
            date_str = future_date.strftime('%Y-%m-%d')
            
            if date_str in self.schedule_data:
                plan = self.schedule_data[date_str]
                # Canadian on a Budget Mentor Summary
                summary = (
                    f"\n📅 **{future_date.strftime('%A, %b %d')}**:\n"
                    f"  Budget Focus: {plan['daily_budget_allocation']} | Plan: Spend only ${plan['daily_total_spent']:.2f}.\n"
                    f"  Key Activity: {plan['activities'][4]['event'].replace('***_', '').replace('_***', '')} @ {plan['activities'][4]['location']}\n"
                    f"  Meal Ticket Use: YES (Breakfast/Dinner).\n"
                )
                lookahead_summary += summary
            else:
                lookahead_summary += f"\n📅 **{future_date.strftime('%A, %b %d')}**: (Data not yet generated - plan only covers the next 15 days from start)."

        self.lookahead_text.config(text=lookahead_summary, justify=tk.LEFT)
        self.after(86400000, self.update_daily_lookahead) # Schedule next update in 24 hours

# --- MAIN APPLICATION ---

class BudgetingProfessorApp(tk.Tk):
    """
    The main application class, embodying the high-level, professor-type code
    requested for structuring the budgeting tool.
    """
    def __init__(self):
        super().__init__()
        self.title("Python3 GUI: Gemini AI Budgeting Mentor")
        self.geometry("800x900")
        self.configure(bg='#F3F4F6')

        # Initialize Core Logic
        self.mentor = BudgetMentor(self)

        # Build UI Components
        self.create_widgets()
        
        # Initial data load
        self.calendar_view.load_schedule(self.mentor.current_schedule)

    def create_widgets(self):
        # 1. ETH Tracker Banner
        self.eth_tracker = EthereumTracker(self, Config.ETH_START_PRICE_USD)

        # 2. Main Budget Summary Panel
        summary_frame = ttk.LabelFrame(self, text="Monthly Budgeting Summary (Until Dec 16)", padding="10")
        summary_frame.pack(fill='x', pady=5, padx=10)
        
        summary_data = self.mentor.get_budget_summary()
        row = 0
        for key, value in summary_data.items():
            tk.Label(summary_frame, text=f"{key.replace('_', ' ')}:", font=('Inter', 10, 'bold'), anchor='w').grid(row=row, column=0, sticky='w', padx=5, pady=2)
            tk.Label(summary_frame, text=value, font=('Inter', 10), anchor='e', fg='#10B981' if 'Available' in key or 'Target' in key else '#374151').grid(row=row, column=1, sticky='e', padx=5, pady=2)
            row += 1

        # 3. Calendar View (including 3-day lookahead)
        self.calendar_view = CalendarView(self)

        # 4. Action Button
        action_frame = tk.Frame(self, bg='#F3F4F6')
        action_frame.pack(fill='x', pady=10)
        
        ttk.Button(action_frame, 
                   text="Generate/Update Budgeting Plan (Call Gemini AI)", 
                   command=self.mentor.update_schedule,
                   style='Primary.TButton').pack(pady=5)
        
        # Custom Style for the button
        self.style = ttk.Style()
        self.style.configure('Primary.TButton', font=('Inter', 12, 'bold'), 
                             foreground='white', background='#4F46E5', 
                             padding=10)
        self.style.map('Primary.TButton', 
                       background=[('active', '#3730A3')], 
                       foreground=[('active', 'white')])


if __name__ == '__main__':
    app = BudgetingProfessorApp()
    app.mainloop()
