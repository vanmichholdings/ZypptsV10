#!/usr/bin/env python3
"""
Script to create Mike's admin user account
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_mike_admin():
    """Create Mike's admin user account"""
    
    try:
        # Import Flask app and models
        from app_config import create_app
        from models import db, User, Subscription
        
        # Create app context
        app = create_app()
        
        with app.app_context():
            # Check if Mike's admin user already exists
            mike_email = "mike@usezyppts.com"
            existing_mike = User.query.filter_by(email=mike_email).first()
            
            if existing_mike:
                print(f"✅ Mike's admin user already exists: {mike_email}")
                print(f"   Username: {existing_mike.username}")
                print(f"   Admin status: {existing_mike.is_admin}")
                print(f"   Active status: {existing_mike.is_active}")
                
                # Ensure admin privileges are set
                if not existing_mike.is_admin:
                    existing_mike.is_admin = True
                    db.session.commit()
                    print("✅ Admin privileges granted to existing user")
                
                # Check subscription
                if existing_mike.subscription:
                    print(f"   Subscription: {existing_mike.subscription.plan} ({existing_mike.subscription.status})")
                else:
                    # Create subscription for existing user
                    mike_subscription = Subscription(
                        user_id=existing_mike.id,
                        plan='enterprise',
                        status='active',
                        monthly_credits=999999,
                        used_credits=0,
                        start_date=datetime.utcnow(),
                        auto_renew=True
                    )
                    db.session.add(mike_subscription)
                    db.session.commit()
                    print("✅ Enterprise subscription created for existing user")
                
                return existing_mike
            
            # Create new Mike admin user
            mike_user = User(
                username="mike",
                email=mike_email,
                is_admin=True,
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            mike_user.set_password("mike123")  # Change this in production!
            
            # Add to database
            db.session.add(mike_user)
            db.session.commit()
            
            print("✅ Mike's admin user created successfully!")
            print(f"   Email: {mike_email}")
            print(f"   Username: mike")
            print(f"   Password: mike123")
            print(f"   Admin status: {mike_user.is_admin}")
            print("\n⚠️  IMPORTANT: Change the password in production!")
            
            # Create a subscription for Mike
            mike_subscription = Subscription(
                user_id=mike_user.id,
                plan='enterprise',
                status='active',
                monthly_credits=999999,
                used_credits=0,
                start_date=datetime.utcnow(),
                auto_renew=True
            )
            
            db.session.add(mike_subscription)
            db.session.commit()
            
            print("✅ Enterprise subscription created for Mike")
            
            return mike_user
            
    except Exception as e:
        print(f"❌ Error creating Mike's admin user: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔧 Creating Mike's Admin User Account")
    print("=" * 40)
    create_mike_admin()
    print("\n🎯 Next Steps:")
    print("   1. Deploy the application")
    print("   2. Log in with mike@usezyppts.com / mike123")
    print("   3. Visit: https://your-app.fly.dev/admin/")
    print("   4. Change the password in the admin panel") 