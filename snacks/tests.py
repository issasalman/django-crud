from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Issa", email="Issa@email.com", password="1999"
        )

        self.snacks = Snack.objects.create(
            title="hotdog", purchaser=self.user, description="Yummy hotdog",
            
        )
     
        Snack.objects.create(
            title="pitza", purchaser=self.user, description="Yummy pitza",
        )
        Snack.objects.create(
            title="homs", purchaser=self.user, description="Yummy homs",
        )
       

    def test_string_representation(self):
        self.assertEqual(str(self.snacks), "hotdog")

    def test_snack_content(self):
        self.assertEqual(f"{self.snacks.title}", "hotdog")
        self.assertEqual(f"{self.snacks.purchaser}", "Issa")
        self.assertEqual(self.snacks.description, "Yummy hotdog")

    def test_snack1_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "homs")
        self.assertTemplateUsed(response, "snack_list.html")
    def test_snack2_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pitza")
        self.assertTemplateUsed(response, "snack_list.html")


    def test_snack1_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/wrong url/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "hotdog")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack2_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="2"))
        no_response = self.client.get("/wrong url/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Yummy pitza")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "faheta",
                "purchaser": self.user.id,
                "description": "YummmmY",
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="4"))
        self.assertContains(response, "YummmmY")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "zenger","purchaser":self.user.id,"description":'It was spicy and crunchy'}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_thing_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)