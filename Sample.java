/*** Fine-grained Reminding Prompting
@param Pay attention to JSONException
*/
public void load(String json) {
  try {
    mChanged = false;
    mModels = new HashMap<Long, JSONObject>();
    JSONObeject modelarray = new JSONObeject(json);
    JSONArray ids = modelarray.names();
    if (ids != null) {
      for (int i = 0; i < ids.length(); i++) {
        String id = ids.getString(i);
        JSONObject o = modelArray.getJSONObject(id);
        if (o.has("id")) {
          mModels.put(o.getLong("id"), o);
        } else {
          System.err.println("JSONObject for ID " + id + " does not
contain 'id' field.");
        }
    }
  } catch (JSONException e) {
    System.err.println("JSON processing error: " + e.getMessage());
  } catch (NullPointerException e) {
    System.err.println("Null value encountered: " + e.getMessage());
  } catch (Exception e) {
    System.err.println("Unexpected error: " + e.getMessage());
  }
}
