import requests
import os
import hashlib
import mimetypes
from urllib.parse import urlparse
from pathlib import Path
import time

class UbuntuImageFetcher:
    
    def __init__(self, directory="Fetched_Images"):
        self.directory = directory
        self.downloaded_hashes = set()
        self.session = requests.Session()
        # Set a respectful User-Agent
        self.session.headers.update({
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Respectful Community Tool)'
        })
        self._load_existing_hashes()
    
    def _load_existing_hashes(self):
        """Load hashes of existing images to prevent duplicates"""
        if os.path.exists(self.directory):
            for filename in os.listdir(self.directory):
                filepath = os.path.join(self.directory, filename)
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'rb') as f:
                            content_hash = hashlib.md5(f.read()).hexdigest()
                            self.downloaded_hashes.add(content_hash)
                    except Exception:
                        continue  # Skip files that can't be read
    
    def _get_content_hash(self, content):
        """Generate MD5 hash of content for duplicate detection"""
        return hashlib.md5(content).hexdigest()
    
    def _is_safe_content_type(self, content_type):
        """Check if the content type is a safe image format"""
        safe_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/bmp', 'image/webp', 'image/svg+xml'
        ]
        return content_type and content_type.lower() in safe_types
    
    def _get_filename_from_url(self, url, content_type=None):
        """Extract or generate appropriate filename from URL"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename in URL, generate one with appropriate extension
        if not filename or '.' not in filename:
            timestamp = int(time.time())
            
            # Try to get extension from content type
            if content_type:
                extension = mimetypes.guess_extension(content_type)
                if extension:
                    filename = f"ubuntu_image_{timestamp}{extension}"
                else:
                    filename = f"ubuntu_image_{timestamp}.jpg"
            else:
                filename = f"ubuntu_image_{timestamp}.jpg"
        
        # Sanitize filename (remove potentially dangerous characters)
        filename = "".join(c for c in filename if c.isalnum() or c in ".-_")
        
        return filename
    
    def _check_response_safety(self, response):
        """Perform safety checks on the response"""
        # Check content type
        content_type = response.headers.get('content-type', '').split(';')[0]
        if not self._is_safe_content_type(content_type):
            raise ValueError(f"Unsafe content type: {content_type}")
        
        # Check content length (prevent extremely large files)
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 50 * 1024 * 1024:  # 50MB limit
            raise ValueError(f"File too large: {content_length} bytes")
        
        return content_type
    
    def fetch_image(self, url):
        """
        Fetch a single image from URL with comprehensive error handling and safety checks
        """
        try:
            print(f"🌍 Connecting to: {url}")
            
            # First, make a HEAD request to check headers
            try:
                head_response = self.session.head(url, timeout=10, allow_redirects=True)
                if head_response.status_code == 200:
                    content_type = self._check_response_safety(head_response)
                    print(f"✓ Content verified: {content_type}")
                else:
                    print(f"⚠ HEAD request failed, proceeding with GET...")
            except Exception as e:
                print(f"⚠ HEAD request failed ({e}), proceeding with GET...")
            
            # Fetch the image
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Safety checks
            content_type = self._check_response_safety(response)
            
            # Check for duplicates
            content_hash = self._get_content_hash(response.content)
            if content_hash in self.downloaded_hashes:
                print(f"⚠ Image already exists (duplicate detected)")
                return False, "Duplicate image"
            
            # Create directory if it doesn't exist
            os.makedirs(self.directory, exist_ok=True)
            
            # Get appropriate filename
            filename = self._get_filename_from_url(url, content_type)
            filepath = os.path.join(self.directory, filename)
            
            # Handle filename conflicts
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Add hash to prevent future duplicates
            self.downloaded_hashes.add(content_hash)
            
            print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
            print(f"✓ Image saved to {filepath}")
            print(f"✓ Size: {len(response.content):,} bytes")
            
            return True, filepath
            
        except requests.exceptions.Timeout:
            return False, "Connection timeout - the server took too long to respond"
        except requests.exceptions.ConnectionError:
            return False, "Connection error - could not reach the server"
        except requests.exceptions.HTTPError as e:
            return False, f"HTTP error: {e}"
        except ValueError as e:
            return False, f"Safety check failed: {e}"
        except PermissionError:
            return False, "Permission denied - cannot write to directory"
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"
    
    def fetch_multiple_images(self, urls):
        """
        Fetch multiple images from a list of URLs
        """
        successful = 0
        failed = 0
        
        print(f"🌐 Preparing to fetch {len(urls)} images...\n")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Processing: {url}")
            success, message = self.fetch_image(url.strip())
            
            if success:
                successful += 1
                print("✅ Success!\n")
            else:
                failed += 1
                print(f"❌ Failed: {message}\n")
            
            # Be respectful - small delay between requests
            if i < len(urls):
                time.sleep(1)
        
        print(f"📊 Summary: {successful} successful, {failed} failed")
        return successful, failed

def main():
    """Main function implementing the Ubuntu philosophy of community and sharing"""
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("\"I am because we are\" - Ubuntu Philosophy\n")
    
    fetcher = UbuntuImageFetcher()
    
    while True:
        print("\nChoose an option:")
        print("1. Fetch single image")
        print("2. Fetch multiple images")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            url = input("\nPlease enter the image URL: ").strip()
            if url:
                success, message = fetcher.fetch_image(url)
                if success:
                    print("\n🤝 Connection strengthened. Community enriched.")
                else:
                    print(f"\n💔 Connection failed: {message}")
            else:
                print("⚠ Please enter a valid URL")
        
        elif choice == '2':
            print("\nEnter image URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                successful, failed = fetcher.fetch_multiple_images(urls)
                print(f"\n🤝 Connections made: {successful}")
                print("Community enriched through shared resources.")
            else:
                print("⚠ No URLs provided")
        
        elif choice == '3':
            print("\n🙏 Thank you for using Ubuntu Image Fetcher")
            print("Remember: 'A person is a person through other persons'")
            break
        
        else:
            print("⚠ Please enter 1, 2, or 3")

if __name__ == "__main__":
    main()