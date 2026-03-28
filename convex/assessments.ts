import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Create a new session
export const createSession = mutation({
  args: { userId: v.optional(v.id("users")) },
  handler: async (ctx, args) => {
    return await ctx.db.insert("sessions", {
      userId: args.userId,
      status: "active",
      createdAt: Date.now(),
    });
  },
});

// Update an assessment or create if not exists
export const saveAssessment = mutation({
  args: {
    sessionId: v.id("sessions"),
    userId: v.optional(v.id("users")),
    symptoms: v.array(v.string()),
    condition: v.optional(v.string()),
    criticality: v.optional(v.string()),
    doctorType: v.optional(v.string()),
    firstAid: v.optional(v.string()),
    mentalHealth: v.optional(
      v.object({
        status: v.string(),
        needsHelp: v.boolean(),
        notes: v.optional(v.string()),
      })
    ),
    rawText: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    // We insert a new assessment record for the session
    return await ctx.db.insert("assessments", {
      sessionId: args.sessionId,
      userId: args.userId,
      symptoms: args.symptoms,
      condition: args.condition,
      criticality: args.criticality,
      doctorType: args.doctorType,
      firstAid: args.firstAid,
      mentalHealth: args.mentalHealth,
      rawText: args.rawText,
      createdAt: Date.now(),
    });
  },
});

// Fetch latest assessment for a session
export const getAssessmentBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("assessments")
      .withIndex("by_session", (q) => q.eq("sessionId", args.sessionId))
      .order("desc")
      .first();
  },
});
