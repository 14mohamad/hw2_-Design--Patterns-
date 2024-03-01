import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from typing import List

class Observer:
    def __init__(self):
        self.notifications_list = []

    def update(self, notification: str):
        pass

class User(Observer):
    def __init__(self, username_str: str, password_str: str):
        super().__init__()
        self.__is_online = False
        self.__username = username_str
        self.__pass = password_str
        self.__posts = []
        self.__followers = []

    def Get_Username(self) -> str:
        return self.__username

    def Get_Pass(self) -> str:
        return self.__pass

    def is_online(self) -> bool:
        return self.__is_online

    def Set_is_online(self, online_status: bool) -> None:
        self.__is_online = online_status

    def __str__(self):
        str = f"User name: {self.__username}, Number of posts: {len(self.__posts)}, " \
               f"Number of followers: {len(self.__followers)}"

        return str
    def print_notifications(self):
        print(f"{self.__username}'s notifications:")
        for notification_str in self.notifications_list:
            print(notification_str)

    def add_follower(self, new_follower: 'Observer'):
        if new_follower not in self.__followers:
            self.__followers.append(new_follower)

    def remove_follower(self, follower_to_remove: 'Observer'):
        if follower_to_remove in self.__followers:
            self.__followers.remove(follower_to_remove)

    def Get_Followers(self) -> 'List':
        return self.__followers

    def follow(self, user_to_follow: 'User'):
        if not self.__is_online:
            pass
        if user_to_follow != self:
            user_to_follow.add_follower(self)
            str = f"{self.Get_Username()} started following {user_to_follow.Get_Username()}"
            print(str)

    def unfollow(self, user_unfollow: 'User') -> None:
        if not self.__is_online:
            pass
        if self in user_unfollow.Get_Followers():
            user_unfollow.remove_follower(self)
            str = f"{self.Get_Username()} unfollowed {user_unfollow.Get_Username()}"
            print(str)

    def update(self, new_notification: str):
        self.notifications_list.append(new_notification)

    def publish_post(self, *args) -> 'Post':
        new_post = PostFactory.publish_post(self, *args)
        self.__posts.append(new_post)
        print(new_post)
        return new_post

    def print_notifications(self):
        print(f"{self.__username}'s notifications:")
        for notification_str in self.notifications_list:
            print(notification_str)

class PostFactory:
    @staticmethod
    def publish_post(user: 'User', *args) -> 'Post':
        post_type = args[0]
        post = None
        if post_type == "Text":
            post = TextPost(user, args[1])
        elif post_type == "Image":
            post = ImagePost(user, args[1])
        elif post_type == "Sale":
            post = SalePost(user, args[1], args[2], args[3])
        post.notify(user, "post", "")
        return post

class Publisher:
    def notify(self, publisher: 'User', notification_type: str, notification_content: str):
        pass

class Post(Publisher):
    def __init__(self, user: 'User'):
        self._publisher = user
        self._likers = []
        self._comments = []

    def Get_Publisher(self) -> 'User':
        return self._publisher

    def notify(self, publisher: 'User', notification_type: str, notification_content: str):
        if notification_type == "post":
            notification = f"{publisher.Get_Username()} has a new post"
            for follower in publisher.Get_Followers():
                follower.update(notification)

        if notification_type == "like":
            notification = f"{publisher.Get_Username()} liked your post"
            self._publisher.update(notification)
            str = f"notification to {self._publisher.Get_Username()}: {publisher.Get_Username()} liked your post"
            print(str)

        if notification_type == "comment":
            notification = f"{publisher.Get_Username()} commented on your post"
            self._publisher.update(notification)
            str = f"notification to {self._publisher.Get_Username()}: " f"{publisher.Get_Username()} commented on your post: {notification_content}"
            print(str)

    def like(self, liker: 'User'):
        if liker.is_online() and liker not in self._likers and self._publisher != liker:
            self._likers.append(liker)
            self.notify(liker, "like", "")

    def comment(self, commenter: 'User', content: str):
        if commenter.is_online():
            self._comments.append((commenter, content))
            if self._publisher != commenter:
                self.notify(commenter, "comment", content)

    def sold(self, password: str):
        pass

    def discount(self, percent: int, password: str):
        pass

    def display(self):
        pass

class TextPost(Post):
    def __init__(self, user: 'User', content_str: str):
        super().__init__(user)
        self.__content = "\"" + content_str + "\""

    def __str__(self):
        str = "{} published a post:\n{}\n".format(self.Get_Publisher().Get_Username(), self.__content)
        return str

class ImagePost(Post):
    def __init__(self, user: 'User', path_str: str):
        super().__init__(user)
        self.__path = path_str

    def display(self):
        try:
            img = mpimg.imread(self.__path)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            print("Shows picture")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Picture not found at path: {self.__path}") from e

    def __str__(self):
        str = "{} posted a picture\n".format(self.Get_Publisher().Get_Username())
        return str

class SalePost(Post):
    def __init__(self, user: 'User', description_str: str, price_int: int, town_str: str):
        super().__init__(user)
        self.__description = description_str
        self.__price = price_int
        self.__town = town_str
        self.__is_sold = False

    def discount(self, percentage: int, password_str: str) -> None:
        if not super().Get_Publisher().is_online():
            pass
        elif password_str == self.Get_Publisher().Get_Pass() and percentage <= 100:
            self.__price = float(self.__price) * (float(100 - percentage) / 100)
            str = "Discount on {} product! the new price is: {}".format(self.Get_Publisher().Get_Username(), self.__price)
            print(str)

    def sold(self, pass_str: str) -> None:
        if not super().Get_Publisher().is_online():
            pass
        elif pass_str == self.Get_Publisher().Get_Pass():
            self.__is_sold = True
            str = "{}'s product is sold".format(self.Get_Publisher().Get_Username())
            print(str)

    def __str__(self):
        status = "Sold!" if self.__is_sold else "For sale!"
        str = f"{self.Get_Publisher().Get_Username()} posted a product for sale:\n{status} {self.__description}," \
               f" price: {self.__price}, pickup from: {self.__town}\n"
        return str

class SocialNetwork:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SocialNetwork, cls).__new__(cls)
        return cls.instance

    def __init__(self, network_name: str):
        if not hasattr(self, 'initialized'):
            self._name = network_name
            self._users_list: List[User] = []
            self._online_users_list: List[User] = []
            self.initialized = True
            str = f"The social network {self._name} was created!"
            print(str)

    def sign_up(self, username: str, password: str) -> User:
        for signed_user in self._users_list:
            if signed_user.Get_Username() == username:
                pass
        if len(password) < 4 or len(password) > 8:
            pass

        user = User(username, password)
        self._users_list.append(user)
        self._online_users_list.append(user)
        user.Set_is_online(True)
        return user

    def log_in(self, username: str, password: str):
        for signed_user in self._users_list:
            if signed_user.Get_Username() == username and signed_user.Get_Pass() == password:
                if signed_user not in self._online_users_list:
                    self._online_users_list.append(signed_user)
                    signed_user.Set_is_online(True)
                    str = f"{signed_user.Get_Username()} connected"
                    print(str)

    def log_out(self, username: str):
        for online_user in self._online_users_list:
            if online_user.Get_Username() == username:
                self._online_users_list.remove(online_user)
                online_user.Set_is_online(False)
                str = f"{online_user.Get_Username()} disconnected"
                print(str)

    def __str__(self) -> str:
        result = f"{self._name} social network:"
        for user in self._users_list:
            result += f"\n{user}"
        result += "\n"
        return result
