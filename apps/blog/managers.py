from django.db.models import Manager


class PostManager(Manager):
    """Post Manager class"""

    def post_to_frontpage(self):
        """Return the first Post by date published"""
        return self.filter(is_public=True, is_front_page=True).order_by('-created').first()

    def posts_to_home(self):
        """Filter the 4 recent posts"""
        return self.filter(is_public=True).order_by('-created')[:4]

    def recent_posts(self):
        """Filter the 6 recent posts"""
        return self.filter(is_public=True).order_by('-created')[:6]

    
    def search_post(self, kword, topic):
        if len(topic) > 0:
            return self.filter(
                topic__name=topic,
                title__icontains=kword,
                is_public=True
            ).order_by('-created')
        else:
            return self.filter(
                title__icontains=kword,
                is_public=True
            ).order_by('-created')