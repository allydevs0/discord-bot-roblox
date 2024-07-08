### Discord Bot for Roblox User Information

#### Purpose:
- Fetch detailed information about Roblox users and display it on Discord.


**Commands Implemented:**

- `!rouser <username>`
  - Fetches detailed profile information of a Roblox user.
  - Retrieves user ID, display name, creation date, and description.
  - Fetches user's profile picture and collections data.

**API Integration:**
- Interacts with Roblox API endpoints:
  - `https://users.roblox.com/v1/users/search` for basic user info.
  - `https://users.roblox.com/v1/users/{user_id}` for detailed profile.
  - `https://thumbnails.roblox.com/v1/users/avatar-headshot` for user avatars.
  - `https://www.roblox.com/users/profile/robloxcollections-json` for user collections.

**Image Handling:**
- Uses PIL (Python Imaging Library) to create composite images.
- Retrieves collection item thumbnails and combines them into a single image.
- Sends the composite image along with user information as an embed in Discord.

**Embeds and File Sending:**
- Constructs Discord embeds to present fetched user data.
- Attaches composite images of collection items to the embeds.
- Sends the final embed with user information and composite image to Discord.
