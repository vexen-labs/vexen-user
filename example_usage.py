"""
Example usage of vexen-user system.
"""

import asyncio

from vexen_user import VexenUser
from vexen_user.application.dto import CreateUserRequest, UpdateUserRequest


async def main():
	# Initialize VexenUser
	user_system = VexenUser(
		database_url="postgresql+asyncpg://hexa:hexa@localhost/hexa",
		echo=True,  # Show SQL queries
	)

	await user_system.init()

	try:
		print("=" * 80)
		print("VexenUser - Example Usage")
		print("=" * 80)

		# 1. Create users
		print("\n1. Creating users...")
		print("-" * 80)

		user1 = await user_system.service.create(
			CreateUserRequest(
				email="juan.perez@example.com",
				name="Juan Pérez",
				password="SecurePass123!",  # Will be handled by vexen-auth
				role_id="role_admin",
				avatar="https://example.com/avatar1.jpg",
				metadata={"department": "IT", "phone": "+54 11 1234-5678"},
			)
		)

		if user1.success:
			print(f"✅ Created user: {user1.data.name} ({user1.data.email})")
		else:
			print(f"❌ Error: {user1.error}")

		user2 = await user_system.service.create(
			CreateUserRequest(
				email="maria.gonzalez@example.com",
				name="María González",
				password="SecurePass456!",
				role_id="role_operator",
				avatar="https://example.com/avatar2.jpg",
				metadata={"department": "Support", "phone": "+54 11 8765-4321"},
			)
		)

		if user2.success:
			print(f"✅ Created user: {user2.data.name} ({user2.data.email})")

		# 2. List users
		print("\n2. Listing users...")
		print("-" * 80)

		users_list = await user_system.service.list(page=1, page_size=20)

		if users_list.success:
			print(f"Found {users_list.pagination.total_items} users:")
			for user in users_list.data:
				print(f"   - {user.name} ({user.email}) - Status: {user.status}")
			page = users_list.pagination.page
			total = users_list.pagination.total_pages
			print(f"\nPagination: Page {page} of {total}")
		else:
			print(f"❌ Error: {users_list.error}")

		# 3. Get user by ID
		if user1.success:
			print("\n3. Getting user by ID...")
			print("-" * 80)

			user_detail = await user_system.service.get(user1.data.id)

			if user_detail.success:
				print("User Details:")
				print(f"   ID: {user_detail.data.id}")
				print(f"   Name: {user_detail.data.name}")
				print(f"   Email: {user_detail.data.email}")
				print(f"   Role: {user_detail.data.role.display_name}")
				print(f"   Status: {user_detail.data.status}")
				print(f"   Metadata: {user_detail.data.metadata}")
			else:
				print(f"❌ Error: {user_detail.error}")

		# 4. Update user
		if user1.success:
			print("\n4. Updating user...")
			print("-" * 80)

			updated = await user_system.service.update(
				user1.data.id,
				UpdateUserRequest(
					name="Juan Carlos Pérez",
					role_id="role_supervisor",
					status="active",
				),
			)

			if updated.success:
				print(f"✅ Updated user: {updated.data.name}")
			else:
				print(f"❌ Error: {updated.error}")

		# 5. Search users
		print("\n5. Searching users...")
		print("-" * 80)

		search_results = await user_system.service.list(
			page=1, page_size=20, search="juan", status="active"
		)

		if search_results.success:
			print(f"Found {len(search_results.data)} users matching 'juan':")
			for user in search_results.data:
				print(f"   - {user.name} ({user.email})")
		else:
			print(f"❌ Error: {search_results.error}")

		# 6. Get statistics
		print("\n6. Getting user statistics...")
		print("-" * 80)

		stats = await user_system.service.stats()

		if stats.success:
			print("User Statistics:")
			print(f"   Total: {stats.data.total}")
			print(f"   Active: {stats.data.active}")
			print(f"   Inactive: {stats.data.inactive}")
			print(f"   By Role: {stats.data.by_role}")
			print(f"   New this month: {stats.data.new_this_month}")
			print(f"   Recent logins: {stats.data.recent_logins}")
		else:
			print(f"❌ Error: {stats.error}")

		print("\n" + "=" * 80)
		print("✅ Example completed successfully!")
		print("=" * 80)

	finally:
		await user_system.close()


if __name__ == "__main__":
	asyncio.run(main())
