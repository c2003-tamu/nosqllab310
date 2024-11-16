import tkinter as tk
from tkinter import messagebox
#import MongoApp as mongoApp

class VotingApp:
    def __init__(self, root):
        #self.mongoApp = mongoApp.MongoApp()
        self.root = root
        self.root.title("Voter Registration Form")

        # Init size
        self.root.geometry("400x500")

        # UI Elements
        self.voterID_label = tk.Label(root, text="Voter ID:")
        self.voterID_label.pack(padx=10, pady=5)
        self.voterID_entry = tk.Entry(root)
        self.voterID_entry.pack(padx=10, pady=5)

        self.registrationPIN_label = tk.Label(root, text="Registration PIN:")
        self.registrationPIN_label.pack(padx=10, pady=5)
        self.registrationPIN_entry = tk.Entry(root, show="*")  # Hide input as password
        self.registrationPIN_entry.pack(padx=10, pady=5)

        self.candidate_label = tk.Label(root, text="Select 3 Candidates:")
        self.candidate_label.pack(padx=10, pady=5)

        # List of candidates
        #self.candidates = self.mongoApp.get_all_candidates()
        self.candidates = ['A', 'B', 'C', 'D']

        # Variables to store selected candidates
        self.selected_candidates = [tk.StringVar(value="") for _ in range(3)]

        # OptionMenus for selecting candidates
        self.candidate_optionmenus = []
        for i in range(3):
            optionmenu = self.create_optionmenu(i)
            optionmenu.pack(padx=10, pady=5)
            self.candidate_optionmenus.append(optionmenu)

        # Create a frame to contain the buttons and add some spacing
        button_frame = tk.Frame(root)
        button_frame.pack(side="bottom", pady=20)  # Adds space from the bottom of the screen

        # Submit button fixed at the bottom
        self.submit_button = tk.Button(button_frame, text="Submit", command=self.handle_submit)
        self.submit_button.grid(row=0, column=0, padx=10)

        # Reset button fixed at the bottom with some space from submit
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.handle_reset)
        self.reset_button.grid(row=0, column=1, padx=10)

    def create_optionmenu(self, idx):
        """
        Create a new OptionMenu widget for selecting candidates.
        """
        # Get the selected values from all the dropdowns
        selected_values = [var.get() for var in self.selected_candidates]
        
        # Remove empty values from the selected values list
        selected_values = [val for val in selected_values if val != ""]

        # Filter out the already selected candidates from the list of available candidates
        available_candidates = [candidate for candidate in self.candidates if candidate not in selected_values]

        # Create the OptionMenu with the filtered available candidates
        optionmenu = tk.OptionMenu(self.root, self.selected_candidates[idx], *available_candidates, command=self.update_candidate_choices)
        return optionmenu

    def update_candidate_choices(self, *args):
        """
        Update the OptionMenu choices to prevent selecting the same candidate.
        """
        # Destroy existing OptionMenus
        for optionmenu in self.candidate_optionmenus:
            optionmenu.destroy()
        
        # Recreate the OptionMenus with the updated available candidates
        self.candidate_optionmenus.clear()
        for i in range(3):
            optionmenu = self.create_optionmenu(i)
            optionmenu.pack(padx=10, pady=5)
            self.candidate_optionmenus.append(optionmenu)

    def handle_submit(self):
        """
        Handles the submission of the form.
        """
        voter_id = self.voterID_entry.get()
        registration_pin = self.registrationPIN_entry.get()
        candidates = [var.get() for var in self.selected_candidates]

        if not voter_id or not registration_pin or len(set(candidates)) < 3:
            messagebox.showerror("Input Error", "Please provide all fields and select 3 unique candidates.")
            return

        #if self.mongoApp.has_id_voted(voter_id):
        #    messagebox.showerror("Input Error", "You can't vote twice.")

        #try:
        #    self.mongoApp.post_ballot()
        #except Exception as e:
        #    print('Unknown error: ' + str(e))
        
        messagebox.showinfo("Success", f"Vote submitted successfully! Voter ID: {voter_id} has voted for {', '.join(candidates)}")

        # Reset fields after successful submission
        self.handle_reset()

    def handle_reset(self):
        """
        Resets the form fields and dropdown menus.
        """
        self.voterID_entry.delete(0, tk.END)
        self.registrationPIN_entry.delete(0, tk.END)
        for var in self.selected_candidates:
            var.set("")  # Reset the selection for all candidates

        # Call update_candidate_choices to re-enable all candidates in dropdowns
        self.update_candidate_choices()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()
