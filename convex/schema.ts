import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.optional(v.string()),
    email: v.optional(v.string()),
    tokenIdentifier: v.optional(v.string()), // For auth if needed
  }).index("by_token", ["tokenIdentifier"]),

  sessions: defineTable({
    userId: v.optional(v.id("users")), // If anonymous, userId is null
    status: v.string(), // "active", "completed", "error"
    createdAt: v.number(),
  }),

  assessments: defineTable({
    sessionId: v.id("sessions"),
    userId: v.optional(v.id("users")),
    symptoms: v.array(v.string()),
    condition: v.optional(v.string()),
    criticality: v.optional(v.string()), // "Low", "Medium", "High", "Critical"
    doctorType: v.optional(v.string()),
    firstAid: v.optional(v.string()),
    mentalHealth: v.optional(
      v.object({
        status: v.string(),
        needsHelp: v.boolean(),
        notes: v.optional(v.string())
      })
    ),
    rawText: v.optional(v.string()),
    createdAt: v.number(),
  }).index("by_session", ["sessionId"])
    .index("by_user", ["userId"]),
});
