"""Stream type classes for tap-hubspot-sdk."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot_sdk.client import HubspotStream

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


class ListsStream(HubspotStream):
    columns = """
                vid, canonical-vid, merged-vids, portal-id, is-contact, properties
              """

    name = "contact"
    path = "/lists/all/contacts/all?fields={}".format(columns)
    primary_keys = ["addedAt"]
    replication_key = "addedAt"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("vid", IntegerType),
        Property("canonical-vid", IntegerType),
        Property("merged-vids", ArrayType(StringType)),
        Property("portal-id", IntegerType),
        Property("is-contact", BooleanType),
        Property("properties", 
                 ObjectType(Property("lastmodifieddate", StringType),
                            Property("email", StringType),
                            Property("message", StringType),
                            Property("city", StringType),
                            Property("company", StringType),
                            Property("createddate", StringType),
                            Property("firstname", StringType),
                            Property("hs_all_contact_vids", StringType),
                            Property("hs_date_entered_lead", StringType),
                            Property("hs_marketable_reason_id", StringType),
                            Property("hs_is_unworked", StringType),
                            Property("hs_marketable_until_renewal", StringType),
                            Property("hs_latest_source_timestamp", StringType),
                            Property("hs_marketable_reason_type", StringType),
                            Property("hs_marketable_status", StringType),
                            Property("hs_is_contact", StringType),
                            Property("hs_email_domain", StringType),
                            Property("hs_pipeline", StringType),
                            Property("hs_sequences_actively_enrolled_count", StringType),
                            Property("hs_object_id", StringType),
                            Property("hs_time_in_lead", StringType),
                            Property("num_conversion_events", StringType),
                            Property("num_unique_conversion_events", StringType),
                            Property("lastname", StringType),
                            Property("hs_analytics_num_page_views", StringType),
                            Property("hs_analytics_num_event_completions", StringType),
                            Property("hs_analytics_first_timestamp", StringType),
                            Property("hs_social_twitter_clicks", StringType),
                            Property("hs_analytics_num_visits", StringType),
                            Property("twitterprofilephoto", StringType),
                            Property("twitterhandle", StringType),
                            Property("hs_analytics_source_data_2", StringType),
                            Property("hs_social_facebook_clicks", StringType),
                            Property("hs_analytics_source", StringType),
                            Property("hs_analytics_source_data_1", StringType),
                            Property("hs_latest_source", StringType),
                            Property("hs_latest_source_data_1", StringType),
                            Property("hs_latest_source_data_2", StringType),
                            Property("hs_social_google_plus_clicks", StringType),
                            Property("hs_social_num_broadcast_clicks", StringType),
                            Property("state", StringType),
                            Property("hs_social_linkedin_clicks", StringType),
                            Property("hs_lifecyclestage_lead_date", StringType),
                            Property("hs_analytics_revenue", StringType),
                            Property("hs_analytics_average_page_views", StringType),
                            Property("website", StringType),
                            Property("lifecyclestage", StringType),
                            Property("jobtitle", StringType),
                            )
                            
                ),
        Property("form-submissions", ArrayType(StringType)),
        Property("identity-profiles", ArrayType(StringType)),
        Property("merge-audits", ArrayType(StringType)),
        Property("addedAt", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_1", "")
        base_url = "https://api.hubapi.com/contacts/{}".format(version)
        return base_url

    def get_url_params(
            self,
            context: dict | None,  # noqa: ARG002
            next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key    

        params["property"] = "message","email","city","company","createddate","firstname","hs_all_contact_vids","hs_date_entered_lead","hs_marketable_reason_id","hs_is_unworked","hs_marketable_until_renewal","hs_latest_source_timestamp","hs_marketable_reason_type","hs_marketable_status","hs_is_contact","hs_email_domain","hs_pipeline","hs_sequences_actively_enrolled_count","hs_object_id","hs_time_in_lead","num_conversion_events","num_unique_conversion_events","lastname","hs_analytics_num_page_views","hs_analytics_num_event_completions","hs_analytics_first_timestamp","hs_social_twitter_clicks","hs_analytics_num_visits","twitterprofilephoto","twitterhandle","hs_analytics_source_data_2","hs_social_facebook_clicks","hs_analytics_source","hs_analytics_source_data_1","hs_latest_source","hs_latest_source_data_1","hs_latest_source_data_2","hs_social_google_plus_clicks","hs_social_num_broadcast_clicks","state","hs_social_linkedin_clicks","hs_lifecyclestage_lead_date","hs_analytics_revenue","hs_analytics_average_page_views","website","lifecyclestage","jobtitle"

        return params
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("contacts") is not None:
            results = resp_json["contacts"]
        else:
            results = resp_json

        yield from results
    
class UsersStream(HubspotStream):
    columns = """
                id, email, roleIds, primaryteamid
              """

    name = "users"
    path = "/users?fields={}".format(columns)
    primary_keys = ["id"]
    #replication_key = "LastModifiedDate"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("email", StringType),
        Property("roleIds", ArrayType(StringType)),
        Property("primaryteamid", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://api.hubapi.com/settings/{}".format(version)
        return base_url

    def get_url_params(
            self,
            context: dict | None,  # noqa: ARG002
            next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("results") is not None:
            results = resp_json["results"]
        else:
            results = resp_json

        yield from results

                    


